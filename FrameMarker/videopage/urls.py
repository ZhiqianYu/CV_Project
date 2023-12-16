from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views
from homepage import views as homepage_views

urlpatterns = [
    path('', homepage_views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('videolist/', views.video_list, name='video_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
