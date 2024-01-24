from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from annotation.models import FrameAnnotations, VideoFrames
from homepage.models import Video
from django.core.serializers.json import DjangoJSONEncoder
import json

def exportpage(request):
    videos = Video.objects.all().order_by('file_name')

    return render(request, 'exportpage.html', {'videos': videos})

def exportfromselection(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    frame_annotations = FrameAnnotations.objects.filter(video=video).order_by('frame_number', 'frame_type')
    frame_annotations_json = json.dumps(list(frame_annotations.values()), cls=DjangoJSONEncoder)
    video_frames = VideoFrames.objects.filter(video=video).first()

    context = {
        'video': video,
        'frame_annotations': frame_annotations,
        'frame_annotations_json': frame_annotations_json,
        'video_frames': video_frames,
    }

    return render(request, 'exportpage.html', context)

def exportfromannotation(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    frame_annotations = FrameAnnotations.objects.filter(video=video).order_by('frame_number', 'frame_type')
    frame_annotations_json = json.dumps(list(frame_annotations.values()), cls=DjangoJSONEncoder)
    video_frames = VideoFrames.objects.filter(video=video).first()

    context = {
        'video': video,
        'frame_annotations': frame_annotations,
        'frame_annotations_json': frame_annotations_json,
        'video_frames': video_frames,
    }

    return render(request, 'exportpage.html', context)