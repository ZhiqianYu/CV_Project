from django.urls import re_path, path
from . import views

urlpatterns = [
    path('exportpage/select/<int:video_id>/', views.exportfromselection, name='exportfromselection'),
]