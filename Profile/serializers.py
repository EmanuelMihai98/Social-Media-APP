from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "user", "username", "display_name", "bio", "created_at", "profile_pic",
                  "following_count", "followers_count"]
        read_only_fields= ["user", "created_at"]

    def get_following_count(self, obj):
        return obj.count_following()
    
    def get_followers_count(self, obj):
        return obj.count_followers()