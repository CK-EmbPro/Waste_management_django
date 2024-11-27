from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, "Your account has been registered successfully")
            if user.role == 'collector':
                return redirect("wastes:collector_dashboard")
            else:
                return redirect("wastes:normaluser_dashboard")
        
        
    else: 
        form = CustomUserCreationForm()
        
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    
    form = CustomAuthenticationForm()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(username=username)
            
        except CustomUser.DoesNotExist:
            user = None
        
        if user is not None:
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, "You're now logged in")
                if user.role == 'collector':
                    return redirect("wastes:collector_dashboard")
                else:
                    return redirect("wastes:normaluser_dashboard")
                
            else: 
                messages.error(request, "Invalid username or password")
                
        else:
            messages.error(request, "User with the provided username does not exist")
            
        
    return render(request, "users/login.html", {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("users:user_login")

def home(request):
    users = CustomUser.objects.all()
    return render(request, "users/home.html", {'users': users})
    # return JsonResponse(list(users), safe=False)

