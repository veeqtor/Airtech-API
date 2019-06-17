"""Module for urls for the user API"""

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
]