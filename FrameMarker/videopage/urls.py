from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('videopage', views.index, name='videos'),
    path('', views.redirect_to_home, name='redirect_to_home'), 
]
