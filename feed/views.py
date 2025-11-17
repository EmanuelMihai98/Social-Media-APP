from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Posts.models import Post
from follows.models import Follow


def feed_view(request):
    following_user = Follow.objects.filter(
        follower=request.user
    ).values_list("following", flat=True)

    posts = Post.objects.filter(
        author__in=list(following_user) + [request.user]
    ).order_by("-created_at")

    context = {
        "posts": posts
    }

    return render(request, "feed/feed.html", context)


