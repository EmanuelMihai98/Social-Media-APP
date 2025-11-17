from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (ProfileViewSet, 
                    profile_view,
                    profile_edit,
                    user_register,
                    user_login,
                    user_logout)

router=DefaultRouter()
router.register(r'', ProfileViewSet, basename="Profile")

api_urlpatterns = router.urls

web_urlpatterns = [
    path("register/", user_register, name="user_register"),
    path("login/", user_login, name="user_login"),
    path("logout/", user_logout, name="user_logout"),
    
    path("edit/", profile_edit, name="profile_edit"),
    path("<str:username>/", profile_view, name="profile_view"),

         
]


urlpatterns = api_urlpatterns + web_urlpatterns