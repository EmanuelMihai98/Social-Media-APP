from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    username_author = serializers.CharField(source="author.username", read_only=True)
    count_likes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["username_author", "author", "created_at", "updated_at", "post", "text", "count_likes"]
        read_only_fields = ["author", "created_at", "updated_at"]

    def get_count_likes(self, obj):
        return obj.likes_count()