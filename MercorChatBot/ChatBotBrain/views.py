from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Chat
from .utils import ChatBotQuery
from datetime import datetime


class ChatBotBrainView(APIView):

    def post(self, request):
        body = request.data
        query = body.get('query')
        chat_id = body.get('chat_id')
        if not chat_id:
            return Response({"error": "chat_id is required"}, status=400)

        chat = Chat.objects.filter(chat_id=chat_id)
        if not chat.exists():
            return Response({"error": "chat_id not found"}, status=404)

        chat_bot_query = ChatBotQuery(chat_id)

        chat = chat.first()
        messages = chat.messages
        cur_message = {
            "sender": "user",
            "message": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        messages.append(cur_message)

        result = chat_bot_query.query_pinecone(query)

        cur_message = {
            "sender": "bot",
            "message": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        messages.append(cur_message)

        Chat.objects.filter(chat_id=chat_id).update(messages=messages)
        return Response(result)


class ChatView(APIView):
    def post(self, request):
        chat = Chat.objects.create(messages=[])
        chat_id = chat.chat_id
        return Response({"chat_id": chat_id})

    def get(self, request):
        type = request.query_params.get('type')
        if type == "ALL":
            chats = Chat.objects.all().values("chat_id", "created_at")
            return Response(chats)
        chat_id = request.query_params.get('chat_id')
        messages = Chat.objects.filter(chat_id=chat_id).values("messages")

        return Response(messages)
