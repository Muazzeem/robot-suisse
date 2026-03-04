from django.urls import path
from .views import post_output, get_chat

app_name = "chat"

urlpatterns = [
    path('', get_chat, name='get-chat'),
    path('send-result/', post_output, name='send-result'),
]
