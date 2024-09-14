from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone
from main import query_api

history = []

# Create your views here.
def home(request):
    return render(request, 'docsai/home.html')


def rag(request):
    if not request.user.is_authenticated:
        return redirect('login')
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = query_api(message, history)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'docsai/chat.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chat')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'docsai/login.html', {'error_message': error_message})
    else:
        return render(request, 'docsai/login.html')

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
                return redirect('chat')
            except:
                error_message = 'Error in creating the account'
                return render(request, 'docsai/register.html', {'error_message': error_message})
        else:
            error_message = "Password doesn't match"
            return render(request, 'docsai/register.html', {'error_message': error_message})
    return render(request, 'docsai/register.html')

def logout(request):
    auth.logout(request)
    return redirect('home')