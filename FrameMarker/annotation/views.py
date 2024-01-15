import os
import cv2
from django.shortcuts import render, get_object_or_404
from homepage.models import Video
from .models import VideoFrames
from django.conf import settings

def annotation(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    filename = video.file_name
    uploader = video.uploader
    video_frames = VideoFrames.objects.filter(video=video)

    print(f"Number of frames in database: {video_frames.count()}")

    if not (video_frames.filter(has_frames_60=True).exists() and video_frames.filter(has_frames_4=True).exists()):
        print("Frames not found or not all frames are generated. Generating frames...")
        uploadtime = video.upload_time.strftime('%Y%m%d%H%M%S')
        generate_frames(video, filename, uploadtime)
    else:
        print("Frames already exist and are generated.")

    return render(request, 'annotation.html', {'video': video, 'filename': filename, 'uploader': uploader})

def generate_frames(video, filename, uploadtime):
    video_file_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
    cap = cv2.VideoCapture(video_file_path)

    folder_name = f"{filename[:10].replace(' ', '')}-{video.uploader.username}-{uploadtime}"

    frame_folder_4 = os.path.join(settings.MEDIA_ROOT, 'Frames', folder_name, '4')
    frame_folder_60 = os.path.join(settings.MEDIA_ROOT, 'Frames', folder_name, '60')
    os.makedirs(frame_folder_4, exist_ok=True)
    os.makedirs(frame_folder_60, exist_ok=True)

    frame_number = 0
    total_frames_60 = 0
    total_frames_4 = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_number % 60 == 0:
            frame_path = os.path.join(frame_folder_60, f'frame_60_{frame_number}.png')
            cv2.imwrite(frame_path, frame)

            video_frame = VideoFrames(
                video=video,
                has_frames_60=True,
                frame_folder_path=frame_folder_60,
                frame_number=frame_number,
            )
            video_frame.save()
            total_frames_60 += 1

        if frame_number % 4 == 0 and frame_number % 60 != 0:
            frame_path = os.path.join(frame_folder_4, f'frame_4_{frame_number}.png')
            cv2.imwrite(frame_path, frame)

            video_frame = VideoFrames(
                video=video,
                has_frames_4=True,
                frame_folder_path=frame_folder_4,
                frame_number=frame_number,
            )
            video_frame.save()
            total_frames_4 += 1

        frame_number += 1

    print(f"Total frames 60: {total_frames_60}")
    print(f"Total frames 4: {total_frames_4}")

    # Update total frames in the VideoFrames model
    video_frames = VideoFrames.objects.filter(video=video)
    if video_frames.exists():
        video_frame = video_frames.first()
        video_frame.total_frames_60 = total_frames_60
        video_frame.total_frames_4 = total_frames_4
        video_frame.save()
        print(f"Updated total frames in the database: {video_frame.total_frames_60} (60 frames), {video_frame.total_frames_4} (4 frames)")
    cap.release()
