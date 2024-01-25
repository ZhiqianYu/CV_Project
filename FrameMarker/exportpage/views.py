from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from annotation.models import FrameAnnotations, VideoFrames
from homepage.models import Video
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
import json
import csv
import os

def exportpage(request):
    videos = Video.objects.all().order_by('file_name')

    return render(request, 'exportpage.html', {'videos': videos})

def exportpagefromselection(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    frame_annotations = FrameAnnotations.objects.filter(video=video).order_by('frame_number', 'frame_type')
    frame_annotations_list = list(frame_annotations.values())
    video_frames = VideoFrames.objects.filter(video=video).first()

    context = {
        'video': video,
        'frame_annotations': frame_annotations,
        'frame_annotations_list': frame_annotations_list,
        'video_frames': video_frames,
        'video_name': video.file_name,
    }

    return render(request, 'exportpage.html', context)

def exportpagefromannotation(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    frame_annotations = FrameAnnotations.objects.filter(video=video).order_by('frame_number', 'frame_type')
    frame_annotations_list = list(frame_annotations.values())
    video_frames = VideoFrames.objects.filter(video=video).first()

    context = {
        'video': video,
        'frame_annotations': frame_annotations,
        'frame_annotations_list': frame_annotations_list,
        'video_frames': video_frames,
        'video_name': video.file_name,
    }

    return render(request, 'exportpage.html', context)

def export_format(request, format, video_id):
    selected_columns = request.GET.get('columns').split(',')

    if format == 'json':
        return exportjson(request, video_id, selected_columns)
    elif format == 'csv':
        return exportcsv(request, video_id, selected_columns)
    else:
        # Handle unsupported format
        return HttpResponse("Unsupported format", status=400)

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