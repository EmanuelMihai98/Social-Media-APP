"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Profile.urls import api_urlpatterns as profile_api_urls 
from Profile.urls import web_urlpatterns as profile_web_urls
from Posts.urls import api_urlpatterns as posts_api_urls
from Posts.urls import web_urlpatterns as posts_web_urls
from comments.urls import api_urlpatterns as comments_api_urls
from comments.urls import web_urlpatterns as comments_web_urls
from .views import home_view, demo_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_view, name="home"),
    path("demo/", demo_login, name="demo_login"),
    path("api/", include([
            path("profiles/", include(profile_api_urls)),
            path("posts/", include(posts_api_urls)),
            path("follows/", include("follows.urls")),
            path("comments/", include(comments_api_urls)),
])),
    path("profile/", include(profile_web_urls)),
    path("posts/", include(posts_web_urls)),
    path("comments/", include(comments_web_urls)),
    path("feed/", include("feed.urls")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    