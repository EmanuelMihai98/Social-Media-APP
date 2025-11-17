from django.db import models
from django.contrib.auth.models import User
from Posts.models import Post

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, related_name="comment_likes", blank=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.author.username}: {self.text[:100]}"

    def likes_count(self):
        return self.likes.count()