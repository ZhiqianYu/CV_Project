from django.urls import path
from . import views

urlpatterns = [
    path('annotation/<int:video_id>/', views.annotation, name='annotation'),
]