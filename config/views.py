from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages

def home_view(request):
    return render(request, "home.html")

def demo_login(request):
    try:
        demo_user = User.objects.get(username="demo")
        login(request, demo_user)
        messages.success(request, "You're now viewing as demo user. Explore the app!")
        return redirect("/feed/")
    
    except User.DoesNotExist:
        messages.error(request, "Demo user not found. Please contact the admin")
        return redirect("/")