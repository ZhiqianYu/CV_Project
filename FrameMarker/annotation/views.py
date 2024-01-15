import os
import cv2
from django.shortcuts import render, get_object_or_404
from homepage.models import Video
from .models import VideoFrames
from django.conf import settings
from django.http import JsonResponse

def annotation(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    filename = video.file_name
    uploader = video.uploader

    return render(request, 'annotation.html', {'video': video, 'filename': filename, 'uploader': uploader})

def generate_frames(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video_frames = VideoFrames.objects.filter(video=video)

    print(f"Number of frames in the database: {video_frames.count()}")

    if not (video_frames.filter(has_frames_60=True).exists() and video_frames.filter(has_frames_4=True).exists()):
        print("Frames not found or not all frames are generated. Generating frames...")
        uploadtime = video.upload_time.strftime('%Y%m%d%H%M%S') 
        
        # Call the separate function for frame generation
        generate_frames_for_video(video, uploadtime)
    else:
        print("Frames already exist and are generated.")
    
    return JsonResponse({'status': 'success'})

def generate_frames_for_video(video, uploadtime):
    video_file_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
    cap = cv2.VideoCapture(video_file_path)

    folder_name = f"{video.file_name[:10].replace(' ', '')}-{video.uploader.username}-{uploadtime}"

    frame_folder = os.path.join(settings.MEDIA_ROOT, 'Frames', folder_name)
    frame_folder_4 = os.path.join(settings.MEDIA_ROOT, 'Frames', folder_name, '4')
    frame_folder_60 = os.path.join(settings.MEDIA_ROOT, 'Frames', folder_name, '60')
    os.makedirs(frame_folder, exist_ok=True)
    os.makedirs(frame_folder_4, exist_ok=True)
    os.makedirs(frame_folder_60, exist_ok=True)

    frame_number = 0
    total_frames_60 = 0
    total_frames_4 = 0

    video_frames, created = VideoFrames.objects.get_or_create(video=video)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_number % 60 == 0:
            frame_path = os.path.join(frame_folder_60, f'frame_60_{frame_number}.png')
            cv2.imwrite(frame_path, frame)
            total_frames_60 += 1

        if frame_number % 4 == 0 and frame_number % 60 != 0:
            frame_path = os.path.join(frame_folder_4, f'frame_4_{frame_number}.png')
            cv2.imwrite(frame_path, frame)
            total_frames_4 += 1

        frame_number += 1

    video_frames.has_frames_60 = total_frames_60 > 0
    video_frames.has_frames_4 = total_frames_4 > 0
    video_frames.total_frames_60 = total_frames_60
    video_frames.total_frames_4 = total_frames_4
    video_frames.video_frames_total = total_frames_60 + total_frames_4
    video_frames.frame_folder_path = frame_folder
    video_frames.frame_folder_path_4 = frame_folder_4
    video_frames.frame_folder_path_60 = frame_folder_60
    video_frames.save()
    cap.release()