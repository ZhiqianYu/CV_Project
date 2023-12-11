from django.urls import re_path, path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    
    # 链接定向，x.x.x.x/...网址显示，来自于views的函数名，name是网址的名字（用于index.html）
    path('', views.homepage, name = 'homepage'),
    path('videos/', views.videopage, name = 'videopage'),
    
    # 处理文件上传
    path('upload/', views.upload_file, name = 'upload_file'),

    # 用户注册
    path('register/', views.register_view, name = 'register'),

    # 用户登录
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
