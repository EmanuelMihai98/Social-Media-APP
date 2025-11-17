from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, comment_edit, comment_delete
from django.urls import path

router = DefaultRouter()
router.register(r'', CommentViewSet, basename="comments")
api_urlpatterns = router.urls

web_urlpatterns = [
    path("<int:pk>/edit/", comment_edit, name="comment_edit"),
    path("<int:pk>/delete/", comment_delete, name="comment_delete")
]

urlpatterns = api_urlpatterns + web_urlpatterns

