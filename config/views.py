from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from Profile.models import Profile
from django.http import HttpResponse

def home_view(request):
    return render(request, "home.html")


def demo_login(request):
    try:
        demo_user = User.objects.get(username="demo")
    except User.DoesNotExist:
        
        demo_user = User.objects.create_user(
            username="demo",
            email="demo@test.com",
            password="demo123",
            first_name="Demo",
            last_name="User"
        )
       
        Profile.objects.get_or_create(
            user=demo_user,
            defaults={'bio': 'Demo user - Try the app! 🎉'}
        )
        messages.info(request, "Demo user created!")
    
    login(request, demo_user, backend='django.contrib.auth.backends.ModelBackend')
    messages.success(request, "You're now viewing as demo user. Explore the app!")
    return redirect("/feed/")
