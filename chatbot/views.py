from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Chat
from .serializers import ChatSerializer
from .msalAuth import msalAuth
from .get_access_token import get_access_token
from .ask_gemini import ask_gemini
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .apiMapping import apiMapping
@csrf_exempt
@api_view(['GET', 'POST'])
def chatbot_api(request):
    if request.method == 'POST':
        message = request.data.get('message')
        if message is not None:
            response = apiMapping(message)
            gemini_response = ask_gemini(response)
            print(gemini_response)
        user = User.objects.get(username='akshay')
        chat = Chat.objects.create(user=user, message=message, response=gemini_response)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)
    elif request.method == 'GET':
        chats = Chat.objects.filter(user=request.user)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)


