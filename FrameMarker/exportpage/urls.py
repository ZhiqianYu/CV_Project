from django.urls import re_path, path

from . import views

urlpatterns = [
    path('exportpage/', views.exportpage, name='exportpage'),
    path('exportpage/<int:video_id>/', views.exportfromannotation, name='exportfromannotation'),
]