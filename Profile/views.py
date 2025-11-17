from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import viewsets
from .forms import ProfileForm, UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from follows.models import Follow
from django.contrib import messages


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

 
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    context = {
        "profile": profile,
        "user": user,
        "is_following": is_following
    }
    return render(request, "Profile/profile.html", context)
    
@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect(f"/profile/{request.user.username}/")
        else:
            messages.error(request, "Error updating profile!")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "Profile/edit.html", {"form": form})

def user_register(request):
    if request.user.is_authenticated:
        return redirect("profile_view", username=request.user.username)
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            login(request, user)

            messages.success(request, f"Your account {username}, has been created!")
            
            return redirect("profile_view", username=username)
        
        else:
            messages.error(request, f"Incorrect credentials. Try again!")

    else:
        form = UserRegisterForm()

    return render(request, "Profile/register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("profile_view", username=request.user.username)
    
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"HELLO, {username}!")

                next_url = request.GET.get("next", f"/profile/{username}")
                return redirect(next_url)
            
        else:
            messages.error(request, "Invalid credentials!")
    else:
        form = UserLoginForm()
    
    return render(request, "Profile/login.html", {"form": form})

@login_required
def user_logout(request):
    username = request.user.username
    logout(request)
    messages.success(request, f"Good-Bye, {username}!")
    return redirect("user_login")


