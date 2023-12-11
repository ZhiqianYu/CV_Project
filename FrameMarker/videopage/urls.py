from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('videos/', views.videopage, name='videopage'), 
]
