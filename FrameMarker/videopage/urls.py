from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='videos'),
    path('upload/', views.upload_video, name='upload_video'),
    path('videos/', views.video_list, name='video_list'),
]
