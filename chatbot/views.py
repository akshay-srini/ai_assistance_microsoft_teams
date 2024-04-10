from django.shortcuts import render, redirect
from django.http import JsonResponse

from .ask_gemini import ask_gemini
from .msalAuth import msalAuth
from .get_access_token import get_access_token
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat


from django.utils import timezone

# pdf_file_path = '/Users/akshaysrinivasan/Downloads/django-chatbot-main/django_chatbot/chatbot/static/assets/Team 16 - Mental health Chatbot.pdf'



# Create your views here.
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    # access_token = msalAuth()
    # return render(request, 'chatbot.html', {'chats':access_token})

    if request.method == 'POST':
        message = request.POST.get('message')
        if message == 'get access token':
            access_token = msalAuth()
            access_token_id = access_token
            response = access_token
        elif message == 'get the user details':
            # print(access_token_id)

            user_details = get_access_token()
            response = user_details
        else:
        # response = PdfReader.extract_text_from_pdf(pdf_file_path)
          response = ask_gemini(message)
          print(response)
        # markdown_response = f"```markdown\n{response}\n```"
# 
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'chats': "response"})
    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        user_id = request.user.id
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
