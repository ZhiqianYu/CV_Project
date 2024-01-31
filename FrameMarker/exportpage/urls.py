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
        Here is just how to load the data from the database and display it on the html page.
        It has two ways to get to this page, one is from navbar, then it requires to load the data mannually.
        One is by click the export button in annotation page, then it will load the data automatically, also there it use the id in the url
        of annotation page. In the whole project, when the id, path, file are sometimes not easy to get, it will get it from the url, html page,
        or the choosed file by resovling the file name and path.
"""

from django.urls import re_path, path
from . import views

urlpatterns = [
    path('exportpage/select/<int:video_id>/', views.exportpagefromselection, name='exportpagefromselection'),
    path('export/<str:format>/<int:video_id>', views.export_format, name='export_format'),
]