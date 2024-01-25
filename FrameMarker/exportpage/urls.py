from django.urls import re_path, path
from . import views

urlpatterns = [
    path('exportpage/select/<int:video_id>/', views.exportpagefromselection, name='exportpagefromselection'),
    path('export/<str:format>/<int:video_id>', views.export_format, name='export_format'),
]