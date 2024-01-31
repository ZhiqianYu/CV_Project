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
        Important here, the html page displayed a lot of infos get from the corresponding model item - video Id. It use this id to
            file name and uploder info and displayed on page. The logic for annotation progress is also here. It get the video id and 
            choosed frame file name, in the frameannotate.js it has the logic to get the type and num and fold of the choosed frames. Then
            load the sub frame with those infos. And while click on rank, it will pass the rank info to the annotate_frame view, and there
            will check the database and write database.
"""

from django.urls import path
from . import views
from homepage import views as homepage_views
from videopage import views as videopage_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from exportpage import views as exportpage_views


urlpatterns = [
    path('', homepage_views.introduction, name = 'introduction'),
    path('uploadpage/', homepage_views.upload, name = 'upload'),
    path('videolist/', videopage_views.video_list, name='video_list'),
    path('annotation/<int:video_id>/', views.annotation, name='annotation'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', homepage_views.register_view, name = 'register'),
    path('generate_frames/<int:video_id>/', views.generate_frames, name='generate_frames'),
    path('annotate_frames/<int:video_id>/<str:frame_type>/<int:frame_number>/<str:rank>/', views.annotate_frames, name='annotate_frames'),
    path('exportpage/anno/<int:video_id>/', exportpage_views.exportpagefromannotation, name='exportpagefromannotation'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)