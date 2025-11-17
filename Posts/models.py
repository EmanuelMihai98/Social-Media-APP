from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.ImageField(upload_to= "post_content/", blank=True)
    content_description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, related_name="likes_posts", blank=True)

    class Meta:
        ordering = ["-created_at"]


    def __str__(self):
        return f" {self.author.username}: {self.content_description[:50]}"
    
    def likes_count(self):
        return self.likes.count()
