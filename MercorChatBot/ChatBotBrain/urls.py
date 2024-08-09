from django.contrib import admin
from django.urls import path
from .views import ChatBotBrainView, ChatView

urlpatterns = [
    path('get-response/', ChatBotBrainView.as_view()),
    path('chat/', ChatView.as_view())
]
