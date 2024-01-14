from django.shortcuts import render, get_object_or_404
from homepage.models import Video

# Create your views here.
def annotation(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    filename = video.file_name
    uploader = video.uploader
    return render(request, 'annotation.html', {'video': video, 'filename': filename, 'uploader': uploader})