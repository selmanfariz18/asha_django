from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse



# Create your views here.


def base(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email=request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            else:
                # create user and profile objects
                user = User.objects.create_user(
                    username=username, password=password,email=email)
                user.save()

                messages.success(request, 'Account created successfully.')
                return render(request, 'register.html')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect('register')
    return render(request, 'register.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)          
            if user.is_superuser:
                messages.error(request, "Password/email incorrect")
                return render(request, 'register.html')
            else:
                return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(request, "Password/email incorrect")
            return render(request, 'register.html')   
        
def edit_profile(request):
    return render(request, 'edit_profile.html')

def home(request):
    return render(request, 'home.html')