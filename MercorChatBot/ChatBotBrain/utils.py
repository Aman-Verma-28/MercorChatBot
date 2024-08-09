import os
from langchain.embeddings.openai import OpenAIEmbeddings
import dotenv
from pinecone import Pinecone
from .models import MercorUserProfile
from openai import OpenAI
import json

dotenv.load_dotenv()


openai_api_key = os.environ.get('OPENAI_API_KEY') or 'OPENAI_API_KEY'
model_name = 'text-embedding-ada-002'
embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=openai_api_key
)
client = OpenAI(api_key=openai_api_key)

pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
index = pc.Index(os.environ.get('PINECONE_INDEX_NAME'))


class ChatBotQuery:
    def __init__(self):
        self.openai_client = client
        self.prompt = """ONLY RESPOND BACK IN PROPER JSON FORMAT. DO NOT GIVE CODE BLOCKS JUST PURE JSON STRING. You are a hiring manager. You are given a query, based on the query you have to respond back.
        in case if the query does not contain information about skills, wages, work experience, give a JSON response back to me
        with a suitable followup message to ask the user for the missing information. the JSON should look like {
        "message": "Please provide any of the following information: skills, wages, work experience to proceed further"
        "status": false}
        else if the query contains information about skills, wages, work experience, give a JSON response back to me
        with {"message": "Thank you for providing the information", "status": true}
        MAKE SURE TO RESPOND BACK IN JSON FORMAT ONLY. 
        Some examples of queries are:
        - “I want to hire someone with experience in Python and Node. My budget is $10000 a month.”
            - The chatbot follows up asking whether the user wants a full-time or part-time worker after showing some results
        - “I want to hire someone who worked at a big tech company. I have an unlimited budget. They should be proficient in Python.”
            - The chatbot follows up asking whether the user wants a full-time or part-time worker after showing some results
        - “I want to hire a developer”
            - The chatbot follows up asking for the skills, budget, and whether the worker is part-time or full-time. The chatbot shows results after skills are provided
        
        HERE IS THE QUERY: """

    def query_pinecone(self, query_text, threshold=0.7):
        chat_response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": self.prompt + query_text}
            ]
        )
        print(chat_response)
        chat_response = json.loads(chat_response.choices[0].message.content)
        if not chat_response['status']:
            return chat_response

        query_embedding = embed.embed_query(query_text)

        result = index.query(vector=query_embedding, top_k=3)["matches"]
        ids = [r.id for r in result if r.score > threshold]
        return list(MercorUserProfile.objects.filter(userid__in=ids).values())
