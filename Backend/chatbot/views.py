from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Chat
from .serializers import ChatSerializer
from .msalAuth import msalAuth
from .Get_access_token import get_access_token
from .ask_gemini import ask_gemini

@api_view(['GET', 'POST'])
def chatbot_api(request):
    if request.method == 'POST':    
        message = request.data.get('message')
        if message == 'get access token':
            access_token = msalAuth()
            access_token_id = access_token
            response = access_token
        elif message == 'get the user details':
            user_details = get_access_token()
            response = user_details
        else:
            response = ask_gemini(message)
            print(response)
            
        chat = Chat.objects.create(user=request.user, message=message, response=response)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)
    elif request.method == 'GET':
        chats = Chat.objects.filter(user=request.user)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

