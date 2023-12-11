from django.urls import re_path, path
from . import views

urlpatterns = [
    
    # 链接定向，x.x.x.x/...网址显示，来自于views的函数名，name是网址的名字（用于index.html）
    path('', views.indexpage, name = 'index'),
    path('videopage/', views.videopage, name = 'videopage'),
    
    # 处理文件上传
    path('upload/', views.upload_file, name = 'upload_file'),
]
