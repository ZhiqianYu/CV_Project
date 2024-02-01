"""
    Project by @ZhiqianYu, https://github.com/ZhiqianYu and
               @DaBaivvi, https://github.com/DaBaivvi
        for the course "Computer Vision - Project" of TU Darmstadt in WS 2023-24, instructed by Yannik Frisch, Henry Krumb.
    
    Description by @Zhiqian Yu:
        This project is a web application for annotating frames of videos to prepare the data for ML.
        It is built with Django. The project is hosted on GitHub: https://github.com/ZhiqianYu/CV_Project, currently private.
        It has the basic function of registering, logging in, uploading videos, list videos, generating frames for videos,
          annotating frames, and exporting the annotations in the required formats.

        The project is divided into 4 apps: homepage, videopage, annotation, and exportpage.
        The homepage app is responsible for the introduction page, uploading videos, registering, and logging in.
        The videopage app is responsible for listing videos with ralated infos, filtering videos, and displaying the annotation progress.
        The annotation app is responsible for generating frames for videos, then annotating frames of videos.
        The exportpage app is responsible for loading the annotation data and exporting the annotations in the required formats.
    
    Introduction of this file:
        This file is the homepage urls.py. It is responsible for routing the requests and all the links in the homepage.
        It first load the introduction page, then accroding to click the upload page, video list page,
         login or registeration page and the export page.
"""

from django.urls import re_path, path
from django.contrib.auth import views as auth_views

from . import views
from videopage import views as videopage_views
from annotation import views as annotation_views
from exportpage import views as exportpage_views

urlpatterns = [
    # 地址栏的显示， 哪个views的哪个函数， 引用这个地址使用的名字
    path('', views.introduction, name = 'introduction'),
    path('uploadpage/', views.upload, name = 'upload'),
    path('upload/', views.upload_file, name = 'upload_file'),
    path('uploadpage/videolist/', videopage_views.video_list, name='video_list'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register_view, name = 'register'),
    path('search/', views.search, name='search'),
    path('exportpage/', exportpage_views.exportpage, name='export')
]
