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
        Here is just how to load the data from the database and display it on the html page. Which is introducted in urls.py.
        Here it defines the choose of format to export. As the annotation data is stored in database, when read it, it's better to 
        transform it into list, then read the list in certain way to get the choosed infos. The info you can choose and how is also defined here.
        More specific, its handled by js to get the choosed columns and formats, then pass it to the views.py to get the data from database and 
        export it. The way to export json is a bit different from csv, json is just leave out some info, and generate the json file. csv 
        involes the csv writer to get correct data. The way to write of how to read the raw data is different.
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from annotation.models import FrameAnnotations, VideoFrames
from homepage.models import Video
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required 
from datetime import datetime
import json
import csv
import os

@login_required(login_url='/login/')
def exportpage(request):
    videos = Video.objects.all().order_by('file_name')

    return render(request, 'exportpage.html', {'videos': videos})

@login_required(login_url='/login/')
def exportpagefromselection(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    frame_annotations = FrameAnnotations.objects.filter(video=video).order_by('frame_number', 'frame_type')
    frame_annotations_list = list(frame_annotations.values())
    video_frames = VideoFrames.objects.filter(video=video).first()
    annotation_progress = video.annotation_progress

    context = {
        'video': video,
        'frame_annotations': frame_annotations,
        'frame_annotations_list': frame_annotations_list,
        'video_frames': video_frames,
        'video_name': video.file_name,
        'annotation_progress': annotation_progress,
    }

    return render(request, 'exportpage.html', context)

@login_required(login_url='/login/')
def exportpagefromannotation(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    frame_annotations = FrameAnnotations.objects.filter(video=video).order_by('frame_number', 'frame_type')
    frame_annotations_list = list(frame_annotations.values())
    video_frames = VideoFrames.objects.filter(video=video).first()
    annotation_progress = video.annotation_progress

    context = {
        'video': video,
        'frame_annotations': frame_annotations,
        'frame_annotations_list': frame_annotations_list,
        'video_frames': video_frames,
        'video_name': video.file_name,
        'annotation_progress': annotation_progress,
    }

    return render(request, 'exportpage.html', context)

@login_required(login_url='/login/')
def export_format(request, format, video_id):    
    selected_columns = request.GET.get('columns').split(',')

    if format == 'json':
        return exportjson(request, video_id, selected_columns)
    elif format == 'csv':
        return exportcsv(request, video_id, selected_columns)
    else:
        # Handle unsupported format
        return HttpResponse("Unsupported format", status=400)

@login_required(login_url='/login/')
def exportjson(request, video_id, selected_columns):
    video = get_object_or_404(Video, pk=video_id)
    frame_annotations = FrameAnnotations.objects.filter(video=video).order_by('frame_number', 'frame_type')
    frame_annotations_list = list(frame_annotations.values())

    selected_data = [{key: item[key] for key in selected_columns} for item in frame_annotations_list]

    response_data = json.dumps(selected_data, cls=DjangoJSONEncoder)

    response = HttpResponse(response_data, content_type='application/json')
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.splitext(video.file_name)[0]
    response['Content-Disposition'] = f'attachment; filename="{filename}_{time}_annotations.json"'
    return response

@login_required(login_url='/login/')
def exportcsv(request, video_id, selected_columns):
    video = get_object_or_404(Video, pk=video_id)
    frame_annotations = FrameAnnotations.objects.filter(video=video).order_by('frame_number', 'frame_type')
    frame_annotations_list = list(frame_annotations.values())

    response = HttpResponse(content_type='text/csv')
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.splitext(video.file_name)[0]
    response['Content-Disposition'] = f'attachment; filename="{filename}_{time}_annotations.csv"'

    writer = csv.writer(response)
    
    # Write header
    writer.writerow(selected_columns)
    
    # Write data
    for item in frame_annotations_list:
        writer.writerow([item[key] for key in selected_columns])

    return response