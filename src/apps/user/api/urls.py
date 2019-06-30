"""Module for urls for the user API"""

from django.urls import path, include
from rest_framework.routers import SimpleRouter

from src.apps.user.api.views import UserLogin, UserRegister
from src.apps.user_profile.api.views import (UserProfileUpdate,
                                             PassportViewSet, ImageUpload)

router = SimpleRouter()
router.register(r'passports', PassportViewSet, basename='passports')

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/', UserProfileUpdate.as_view(), name='profile'),
    path('profile/', include(router.urls), name='passports'),
    path('profile/photo', ImageUpload.as_view(), name='photo'),
]
