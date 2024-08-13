import os
from langchain.embeddings.openai import OpenAIEmbeddings
import dotenv
from pinecone import Pinecone
from .models import MercorUserProfile, Chat
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


class RerankResults:
    EDUCATION_WEIGHT = 1.1
    WORK_EXPERIENCE_WEIGHT = 1.3
    SCORE_WEIGHT = 1.5

    def rerank_results(self, profiles, score_mapping):
        for profile in profiles:
            profile['score'] = score_mapping[profile['userid']]
            profile['weight'] = profile['score'] * self.SCORE_WEIGHT + len(
                profile['education']) * self.EDUCATION_WEIGHT + len(
                profile['workExperience']) * self.WORK_EXPERIENCE_WEIGHT
        profiles = sorted(profiles, key=lambda x: x['weight'], reverse=True)
        return profiles


class ChatBotQuery:
    def __init__(self, chat_id=""):
        self.openai_client = client
        self.chat_id = chat_id
        chat = Chat.objects.filter(chat_id=chat_id).first()
        previous_message = chat.messages if chat else []
        previous_message.reverse()
        previous_messages = "\n".join([f"{m['sender']}: {m['message']}"
                                       for m in previous_message if m['sender'] == 'user'])

        self.prompt = """ONLY RESPOND BACK IN PROPER JSON FORMAT. DO NOT GIVE CODE BLOCKS JUST PURE JSON STRING. 
        You are a HIRING MANAGER, do not respond with anything outside of your domain. Just return status false and appropriate message
        if you do not have the information.
         You are given a query, extract these fields out of the query:
        - Skills
        - Budget
        - Full time or part time
        If you do not have any of these fields, respond with a message saying that you do not have that field.
        Like this: {"status": false, "message": "Certainly, I can help you. 
        I will need few additional details to proceed further. Can you please provide me with the skills you are looking for?"}
        
        If you do have some of the fields, respond with the fields you have and ask for the missing fields.
        Like this: {"status": true, "meta_data": {"skills": "Python, Django"}, "message": "Certainly, I can help you, 
        here are some recommendations based on the skills you provided. Can you please provide me with the budget and type of job?"}
        
        If you have everything, respond like this: {"status": true, "meta_data": {"skills": "Python, Django", 
        "fullTimeSalary": "$1000", 
        }, "message": "Sure here are the users our system thinks would be good fit: "}
        
        If someone has added any additional information like, they should have worked at big tech companies,
        then just add that as well in the response like this: {"status": true, "skills": "Python, Django",
        "budget": "$1000", "type": "full time", "additional": "Big tech companies like Google, Facebook, Amazon etc."}
        
        HERE ARE THE PREVIOUS MESSAGES WITH THIS PERSON: """ + previous_messages + "\n\n" + """
        
        HERE IS THE QUERY: """

    def query_pinecone(self, query_text, threshold=0.7):
        chat_response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": self.prompt + query_text}
            ]
        )
        chat_response = json.loads(chat_response.choices[0].message.content)
        if not chat_response['status']:
            chat_response["users"] = []
            return chat_response
        print(chat_response)

        query_embedding = embed.embed_query(query_text)

        result = index.query(vector=query_embedding, top_k=3)["matches"]
        ids = [r.id for r in result if r.score > threshold]
        id_score_mapping = {r.id: r.score for r in result if r.score > threshold}
        if not ids:
            return {"status": False, "message": "No relevant information found."}
        return_data = {
            "status": True,
            "message": chat_response.get("message", "Sure, here are the users: ")
        }

        user_profiles = list(MercorUserProfile.objects.filter(userid__in=ids).values())

        reranker = RerankResults()
        user_profiles = reranker.rerank_results(user_profiles, id_score_mapping)

        for user_profile in user_profiles:
            user_profile['workExperience'] = user_profile['workExperience'][:1]
            user_profile['education'] = user_profile['education'][:1]
            user_profile['skills'] = list(set(user_profile['skills']))

        return_data["users"] = user_profiles

        return return_data
