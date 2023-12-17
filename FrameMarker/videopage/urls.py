from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views
from homepage import views as homepage_views
from annotation import views as annotation_view

urlpatterns = [
    path('', homepage_views.index, name='introduction'),
    path('upload/', homepage_views.upload, name='upload'),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('videolist/', views.video_list, name='video_list'),
    path('annotation/<int:video_id>/', annotation_view.annotation, name='annotation'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
