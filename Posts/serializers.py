from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    count_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["author_username", "author", "created_at", "updated_at", "content", "content_description", 
                  "count_likes"]
        read_only_fields = ["author", "created_at", "updated_at"]

    def get_count_likes(self, obj):
        return obj.likes_count()
    
