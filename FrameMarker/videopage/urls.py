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
        Important here, the way to open the annotation page while click on the annotation info on choosed video. It will pass a video id to
            annotation views, and there it get the video object and all the related imgs and data to display on the annotation page. The video
            preview and infos displayed on the html page comes from the linked model item. So it all related to the certain video with the id.
"""

from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from exportpage import views as exportpage_views

from . import views
from homepage import views as homepage_views
from annotation import views as annotation_view

urlpatterns = [
    path('', homepage_views.introduction, name='introduction'),
    path('uploadpage/', homepage_views.upload, name='upload'),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('videolist/', views.video_list, name='video_list'),
    path('annotation/<int:video_id>/', annotation_view.annotation, name='annotation'),
    path('exportpage/', exportpage_views.exportpage, name='exportpage')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
