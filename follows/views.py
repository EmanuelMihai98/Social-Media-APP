from django.shortcuts import render
from .models import Follow
from .serializers import FollowSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def toggle(self, request):
        following_id = request.data.get("following_id")

        if not following_id:
            return Response({"error": "Id not found"}, status=404)
        

        try:
            following_user = User.objects.get(id=following_id)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        

        if request.user == following_user:
            return Response({"error": "Cannot follow yourself"}, status=400)
        
        follow = Follow.objects.filter(
            follower=request.user,
            following=following_user
        ).first()

        if follow:
            follow.delete()
            return Response({
                "status": "unfollowed",
                "followers_count": following_user.profile.count_followers()
            })
        
        else:
            Follow.objects.create(
                follower=request.user,
                following=following_user
            )
            return Response({
                "status": "followed",
                "followers_count": following_user.profile.count_followers()
            })