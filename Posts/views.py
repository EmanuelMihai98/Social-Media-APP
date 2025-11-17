from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .forms import PostForm
from comments.forms import CommentForm

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({"status": "unliked", "likes_count": post.likes.count()})
        else:
            post.likes.add(request.user)
            return Response({"status": "liked", "likes_count": post.likes.count()})

def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    context = {
        "posts": posts
    }
    return render(request, "Posts/list.html", context)

def get_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by("-created_at")

    user_liked = False
    if request.user.is_authenticated:
        user_liked = request.user in post.likes.all()
        
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"/posts/{pk}/")
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect("posts:detail", pk=pk)
        
    else:
        form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "user_liked": user_liked,
    }
    return render(request, "Posts/detail.html", context)


def post_create(request):
    if not request.user.is_authenticated:
        return redirect("posts:list")
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:detail", pk=post.pk)
        
    else:
        form = PostForm()

    return render(request, "Posts/create.html", {"form": form})

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect("posts:detail", pk=pk)
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:detail", pk=pk)
        
    else:
        form = PostForm(instance=post)

    return render(request, "Posts/edit.html", {"form": form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect(f"/posts/{pk}/")
    
    if request.method == "POST":
        post.delete()
        return redirect("/feed/")
    
    return render(request, "Posts/delete.html", {"post": post})
