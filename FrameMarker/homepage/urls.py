from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('videos/', views.redirect_to_videos, name='redirect_to_videos'), 
    # path('exports/', views.export_page, name='export_page'),
]
