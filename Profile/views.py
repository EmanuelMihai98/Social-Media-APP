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
from django.http import HttpResponse
from datetime import datetime, timedelta
import random
from Posts.models import Post
from comments.models import Comment

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
            return redirect(f"/profile/{request.user.username}/")
    
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile/edit.html", {"form": form})

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



def populate_database(request):
    """
    Temporary view to populate database with test data.
    Access via: /populate-db/
    DELETE THIS VIEW AFTER USE for security!
    """
    
    output = []
    output.append("🚀 Starting database population...<br><br>")

    # Create users
    users_data = [
        {"username": "demo", "email": "demo@test.com", "first_name": "Demo", "last_name": "User"},
        {"username": "john_doe", "email": "john@test.com", "first_name": "John", "last_name": "Doe"},
        {"username": "jane_smith", "email": "jane@test.com", "first_name": "Jane", "last_name": "Smith"},
        {"username": "alex_johnson", "email": "alex@test.com", "first_name": "Alex", "last_name": "Johnson"},
        {"username": "sarah_wilson", "email": "sarah@test.com", "first_name": "Sarah", "last_name": "Wilson"},
        {"username": "mike_brown", "email": "mike@test.com", "first_name": "Mike", "last_name": "Brown"},
    ]

    users = []
    output.append("👥 Creating users...<br>")
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data["username"],
            defaults={
                "email": user_data["email"],
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
            }
        )
        if created:
            user.set_password("demo123")
            user.save()
            output.append(f"  ✅ Created user: {user.username}<br>")
        else:
            output.append(f"  ℹ️  User already exists: {user.username}<br>")
        users.append(user)

    # Update profiles
    bios = [
        "Welcome to my profile! 🎉 Love sharing moments from my life.",
        "Tech enthusiast | Coffee lover ☕ | Sharing my journey",
        "Creative soul 🎨 | Photography | Travel | Food",
        "Fitness & wellness advocate 💪 | Living my best life",
        "Bookworm 📚 | Movie buff 🎬 | Always learning",
        "Entrepreneur | Motivational speaker | Dream big 🚀",
    ]

    output.append("<br>📝 Updating profiles...<br>")
    for user, bio in zip(users, bios):
        profile, created = Profile.objects.get_or_create(user=user)
        profile.bio = bio
        profile.save()
        output.append(f"  ✅ Updated profile for: {user.username}<br>")

    # Create posts
    output.append("<br>📸 Creating posts...<br>")
    posts_data = [
        "Just deployed my first app on Railway! 🚀 Feeling accomplished!",
        "Beautiful sunset today 🌅 Nature is amazing!",
        "Coffee and code - perfect combination ☕💻",
        "Finished reading an amazing book today 📚",
        "New recipe tried and it was delicious! 🍝",
        "Gym session completed 💪 Consistency is key!",
        "Excited for the weekend! Any plans? 🎉",
        "Learning Django has been such a great experience 🐍",
        "Travel is the only thing you buy that makes you richer ✈️",
        "Good vibes only! 😎",
        "Working on something exciting. Stay tuned! 👀",
        "Grateful for all the support from this amazing community ❤️",
        "Monday motivation: You got this! 💯",
        "Best pizza in town! 🍕 Where's your favorite spot?",
        "Coding late into the night 🌙💻",
    ]

    posts = []
    for i, content in enumerate(posts_data):
        user = users[i % len(users)]
        post = Post.objects.create(
            user=user,
            content=content,
            created_at=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        posts.append(post)
        output.append(f"  ✅ Created post by {user.username}<br>")

    # Create follows
    output.append("<br>🤝 Creating follow relationships...<br>")
    demo_user = users[0]
    for user in users[1:]:
        Follow.objects.get_or_create(follower=user, following=demo_user)
        Follow.objects.get_or_create(follower=demo_user, following=user)
        output.append(f"  ✅ {user.username} ↔️ {demo_user.username}<br>")

    for _ in range(10):
        follower = random.choice(users)
        following = random.choice(users)
        if follower != following:
            Follow.objects.get_or_create(follower=follower, following=following)

    # Create comments
    output.append("<br>💬 Creating comments...<br>")
    comments_data = [
        "Great post! 👍", "Love this! ❤️", "Thanks for sharing!",
        "Awesome! 🔥", "So relatable!", "Keep it up! 💪",
        "Inspiring! ✨", "This made my day! 😊", "Totally agree!", "Amazing content! 🌟",
    ]

    for post in posts[:10]:
        num_comments = random.randint(1, 4)
        for _ in range(num_comments):
            commenter = random.choice(users)
            content = random.choice(comments_data)
            Comment.objects.create(
                post=post,
                user=commenter,
                content=content,
                created_at=datetime.now() - timedelta(days=random.randint(0, 15))
            )
        output.append(f"  ✅ Added {num_comments} comments to post<br>")

    output.append("<br>✨ Database population completed!<br>")
    output.append(f"<br>📊 Summary:<br>")
    output.append(f"  👥 Users: {len(users)}<br>")
    output.append(f"  📸 Posts: {len(posts)}<br>")
    output.append(f"  🤝 Follows: {Follow.objects.count()}<br>")
    output.append(f"  💬 Comments: {Comment.objects.count()}<br>")
    output.append("<br>🔑 Login credentials:<br>")
    output.append("  Username: demo<br>")
    output.append("  Password: demo123<br>")
    output.append("<br>⚠️ IMPORTANT: Delete this view and URL after use for security!")

    return HttpResponse("".join(output))