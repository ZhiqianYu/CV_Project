from django.urls import re_path, path
from django.contrib.auth import views as auth_views

from . import views
from videopage import views as videopage_views
from annotation import views as annotation_view

urlpatterns = [
    # 地址栏的显示， 哪个views的哪个函数， 引用这个地址使用的名字
    path('', views.introduction, name = 'introduction'),
    path('uploadpage/', views.upload, name = 'upload'),
    path('upload/', views.upload_file, name = 'upload_file'),
    path('uploadpage/videolist/', videopage_views.video_list, name='video_list'),
    path('annotation/', annotation_view.annotation, name='annotation'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register_view, name = 'register'),
]
