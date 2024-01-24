from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from annotation.models import FrameAnnotations, VideoFrames
from homepage.models import Video

def exportpage(request):
    videos = Video.objects.all()
    return render(request, 'exportpage.html', {'videos': videos})

def exportfromannotation(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    frame_annotations = FrameAnnotations.objects.filter(video=video)
    frame_annotations = frame_annotations.order_by('frame_number', 'frame_type')
    video_frames = VideoFrames.objects.filter(video=video).first()

    context = {
        'video': video,
        'frame_annotations': frame_annotations,
        'video_frames': video_frames,
    }

    return render(request, 'exportpage.html', context)