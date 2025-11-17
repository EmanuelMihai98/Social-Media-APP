from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .forms import CommentForm

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def likes(self, request, pk=None):
        comment = self.get_object()

        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response({
                "status": "unliked",
                "likes_count": comment.likes.count()
            })
        
        else:
            comment.likes.add(request.user)
            return Response({
                "status": "liked",
                "likes_count": comment.likes.count()
            })
        

def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author != request.user:
        return redirect("post-detail", pk=comment.post.pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("post-detail", pk=comment.post.pk)
        
    else:
        form = CommentForm(instance=comment)

    context = {
        "form": form,
        "comment": comment,
        "post": comment.post
    }

    return render(request, "comments/edit.html", context)

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk

    if comment.author != request.user:
        return redirect("post-detail", pk=post_pk)
    
    if request.method == "POST":
        comment.delete()
        return redirect("post-detail", pk=post_pk)
    
    context = {
        "comment": comment,
        "post": comment.post
    }

    return render(request, "comments/delete.html", context)

