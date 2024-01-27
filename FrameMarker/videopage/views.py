from django.shortcuts import render
from homepage.models import Video

import os
from django.conf import settings
from django.shortcuts import render
from .models import Video


def video_list(request):
    # Retrieve all videos from the database
    videos = Video.objects.all()

    # Filter videos based on user-selected criteria
    sort_by = request.GET.get('sort_by')
    name_filter = request.GET.get('filename')
    uploader_filter = request.GET.get('uploader')
    annotated_filter = request.GET.get('annotated')
    order = request.GET.get('order')

    if name_filter:
        videos = videos.filter(file_name__icontains=name_filter)

    if uploader_filter:
        videos = videos.filter(uploader__username=uploader_filter)

    if annotated_filter:
        annotated_filter = annotated_filter.lower() == 'true'
        if annotated_filter:
            videos = videos.filter(annotation_progress__gt=0)
        else:
            videos = videos.filter(annotation_progress=0)



    # Sort videos based on user-selected criteria
    if sort_by == 'file_name':
        if order == 'asc':
            videos = videos.order_by('file_name')
        elif order == 'desc':
            videos = videos.order_by('-file_name')
    elif sort_by == 'uploader':
        if order == 'asc':
            videos = videos.order_by('uploader__username')
        elif order == 'desc':
            videos = videos.order_by('-uploader__username')
    elif sort_by == 'annotation_progress':
        if order == 'asc':
            videos = videos.order_by('annotation_progress')
        elif order == 'desc':
            videos = videos.order_by('-annotation_progress')

    # Get all unique uploaders for the dropdown
    all_uploaders = Video.objects.values('uploader__username').distinct()

    
    # Get the base directory where your media files are stored
    base_media_path = os.path.join(settings.MEDIA_ROOT)

    # Calculate the relative paths for videos and previews
    for video in videos:
        video.video_file_relative_path = os.path.relpath(video.video_file.path, base_media_path)
        video.preview_file_relative_path = os.path.relpath(video.preview_file.path, base_media_path)

    return render(request, 'videos.html', {'videos': videos, 'all_uploaders': all_uploaders})
