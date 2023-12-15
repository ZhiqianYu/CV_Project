from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('videos/<int:pk>/', views.videopage, name='videopage'), 
]
