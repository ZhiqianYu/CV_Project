from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.index, name='videos'),
    path('home/', views.redirect_to_home, name='redirect_to_home'), 
]
