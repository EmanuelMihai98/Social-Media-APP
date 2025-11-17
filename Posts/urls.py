from rest_framework.routers import DefaultRouter
from .views import PostViewSet, post_list, get_post, post_create, edit_post, post_delete
from django.urls import path

app_name = "posts"


router = DefaultRouter()
router.register(r'', PostViewSet, basename="Posts")
api_urlpatterns = router.urls

web_urlpatterns = [
    path("", post_list, name="list"),
    path("create/", post_create, name="create"),
    path("<int:pk>/", get_post, name="detail"),
    path("<int:pk>/edit/", edit_post, name="edit"),
    path("<int:pk>/delete/", post_delete, name="delete"),
]

urlpatterns = api_urlpatterns + web_urlpatterns