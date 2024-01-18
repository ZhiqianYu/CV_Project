from django.shortcuts import render
from homepage.models import Video

import os
from django.conf import settings
from django.shortcuts import render
from .models import Video

def video_list(request):
    try:
        # Get all video information: title, preview image, uploader, and upload time
        videos = Video.objects.all()

        uploader_filter = request.GET.get('uploader', '')
        order_by = request.GET.get('order_by', 'upload_time')
    
        if uploader_filter:
            videos = videos.filter(uploader__username__icontains=uploader_filter)

        if order_by == 'filename':
            videos = videos.order_by('file_name')
        elif order_by == 'upload_time':
            videos = videos.order_by('-upload_time')
        elif order_by == 'is_annotated':
            videos = videos.filter(annotated=True)
        elif order_by == 'not_annotated':
            videos = videos.filter(annotated=False)
    
    except Exception as e:
        print(f"Error retrieving videos: {e}")
        videos = []

    
    # Get the base directory where your media files are stored
    base_media_path = os.path.join(settings.MEDIA_ROOT)

    # Calculate the relative paths for videos and previews
    for video in videos:
        video.video_file_relative_path = os.path.relpath(video.video_file.path, base_media_path)
        video.preview_file_relative_path = os.path.relpath(video.preview_file.path, base_media_path)

    context = {
        'videos': videos,
        'uploader_filter': uploader_filter,
        'order_by': order_by,    
    }

    return render(request, 'videos.html', context)
    # return render(request, 'videos.html', {'videos': videos})
