from django.shortcuts import render
from homepage.models import Video

import os
from django.conf import settings
from django.shortcuts import render
from .models import Video

def video_list(request):
    # Get all video information: title, preview image, uploader, and upload time
    videos = Video.objects.all()

    # Get the base directory where your media files are stored
    base_media_path = os.path.join(settings.MEDIA_ROOT)

    # Calculate the relative paths for videos and previews
    for video in videos:
        video.video_file_relative_path = os.path.relpath(video.video_file.path, base_media_path)
        video.preview_file_relative_path = os.path.relpath(video.preview_file.path, base_media_path)

    return render(request, 'videos.html', {'videos': videos})
