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
        This file is the main urls.py file of the project. It is responsible for routing the requests to the corresponding apps.
        The path is exactly the same as in the address bar. It also includes the urls.py files in the corresponding apps.
        As this web app is working all the time with videos and imgs so it needs the static() function to serve the media files.
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

    # user defined apps: the path is exactly the same as in address bar
    # and include the urls.py files in corresponding app
    path('', include('homepage.urls')),
    path('', include('videopage.urls')),
    path('', include('annotation.urls')),
    path('', include('exportpage.urls')),
    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
