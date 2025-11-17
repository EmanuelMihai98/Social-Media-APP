# Salvează ca: Profile/management/commands/populate_db.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Profile.models import Profile
from Posts.models import Post
from follows.models import Follow
from comments.models import Comment
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Starting database population...")

        # Create users
        users_data = [
            {"username": "demo", "email": "demo@test.com", "first_name": "Demo", "last_name": "User"},
            {"username": "john_doe", "email": "john@test.com", "first_name": "John", "last_name": "Doe"},
            {"username": "jane_smith", "email": "jane@test.com", "first_name": "Jane", "last_name": "Smith"},
            {"username": "alex_johnson", "email": "alex@test.com", "first_name": "Alex", "last_name": "Johnson"},
            {"username": "sarah_wilson", "email": "sarah@test.com", "first_name": "Sarah", "last_name": "Wilson"},
        ]

        users = []
        self.stdout.write("\n👥 Creating users...")
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
                self.stdout.write(f"  ✅ Created user: {user.username}")
            else:
                self.stdout.write(f"  ℹ️  User exists: {user.username}")
            users.append(user)

        # Update profiles
        bios = [
            "Welcome to my profile! 🎉",
            "Tech enthusiast ☕",
            "Creative soul 🎨",
            "Fitness advocate 💪",
            "Bookworm 📚",
        ]

        self.stdout.write("\n📝 Updating profiles...")
        for user, bio in zip(users, bios):
            profile, created = Profile.objects.get_or_create(user=user)
            profile.bio = bio
            profile.save()

        # Create posts
        self.stdout.write("\n📸 Creating posts...")
        posts_data = [
            "Just deployed my app! 🚀",
            "Beautiful sunset 🌅",
            "Coffee and code ☕💻",
            "Finished a great book 📚",
            "Gym completed 💪",
            "Weekend vibes! 🎉",
            "Learning Django 🐍",
            "Good vibes only! 😎",
            "Monday motivation 💯",
            "Late night coding 🌙",
        ]

        for i, content in enumerate(posts_data):
            user = users[i % len(users)]
            Post.objects.create(user=user, content=content)

        # Create follows
        self.stdout.write("\n🤝 Creating follows...")
        demo_user = users[0]
        for user in users[1:]:
            Follow.objects.get_or_create(follower=user, following=demo_user)
            Follow.objects.get_or_create(follower=demo_user, following=user)

        # Create comments
        self.stdout.write("\n💬 Creating comments...")
        comments_data = ["Great! 👍", "Love this! ❤️", "Awesome! 🔥", "Nice! ✨"]
        posts = Post.objects.all()[:5]
        
        for post in posts:
            for _ in range(2):
                commenter = random.choice(users)
                Comment.objects.create(post=post, user=commenter, content=content)

        self.stdout.write("\n✨ Done!")
        self.stdout.write(f"  👥 Users: {User.objects.count()}")
        self.stdout.write(f"  📸 Posts: {Post.objects.count()}")
        self.stdout.write(f"  🤝 Follows: {Follow.objects.count()}")
        self.stdout.write(f"  💬 Comments: {Comment.objects.count()}")
        self.stdout.write("\n🔑 Login: demo / demo123")