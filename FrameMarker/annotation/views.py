# views.py
import os
import cv2
from django.shortcuts import render, get_object_or_404
from homepage.models import Video
from .models import VideoFrames, FrameAnnotations
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from concurrent.futures import ThreadPoolExecutor

def annotation(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video_frames, created = VideoFrames.objects.get_or_create(video=video)

    filename = video.file_name
    uploader = video.uploader

    max_frame_number = calculate_max_frame_number(video)
    total_frame_files = video_frames.video_frames_total

    frame_folder_60 = video_frames.frame_folder_path_60
    frame_paths_60_orig = [os.path.join(frame_folder_60, f'frame_60_{i}.png') for i in range(0, max_frame_number, 60)]

    frame_folder_4 = video_frames.frame_folder_path_4
    frame_paths_4 = [os.path.join(frame_folder_4, f'frame_4_{i}.png') for i in range(4, max_frame_number, 4) if i % 60 != 0]

    base_media_path = os.path.join(settings.MEDIA_ROOT)
    frame_paths_60 = []

    for frame_path_60 in frame_paths_60_orig:
        frame_path_60_rel = os.path.relpath(frame_path_60, base_media_path)
        frame_path_60 = frame_path_60_rel
        frame_paths_60 = frame_paths_60 + [frame_path_60]
    

    frame_folder_60_rel = os.path.relpath(frame_folder_60, base_media_path)
    frame_folder_60 = frame_folder_60_rel

    video.video_file_rel_path = os.path.relpath (video.video_file.path, base_media_path)

    return render(request, 'annotation.html', {'video': video, 'filename': filename, 'uploader': uploader, 
                                            'frame_paths_4': frame_paths_4, 'frame_folder_4': frame_folder_4,
                                            'frame_paths_60': frame_paths_60, 'frame_folder_60': frame_folder_60,
                                            'total_frame_files': total_frame_files, 'max_frame_number': max_frame_number})

def generate_frames(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video_frames = VideoFrames.objects.filter(video=video)

    print(f"Number of video need to generate frames: {video_frames.count()}")

    total_frames = calculate_max_frame_number(video)

    if not (video_frames.filter(has_frames_60=True).exists() and video_frames.filter(has_frames_4=True).exists()):
        print("Frames not found or not all frames are generated. Generating frames...")
        uploadtime = video.upload_time.strftime('%Y%m%d%H%M%S') 
        
        # Call the separate function for frame generation
        generate_frames_for_video(video, uploadtime)
    else:
        print("Frames already exist and are generated.")
    
    return JsonResponse({'status': 'success', 'total_frames': total_frames})

def calculate_max_frame_number(video):
    video_file_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
    cap = cv2.VideoCapture(video_file_path)
    max_frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return max_frame_number

def generate_frames_for_video(video, uploadtime, num_threads=4):

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

    def process_frame(frame_number, frame, frame_folder_4, frame_folder_60):
        nonlocal total_frames_60, total_frames_4
        if frame_number % 60 == 0:
            frame_path = os.path.join(frame_folder_60, f'frame_60_{frame_number}.png')
            cv2.imwrite(frame_path, frame)
            total_frames_60 += 1

        if frame_number % 4 == 0 and frame_number % 60 != 0:
            frame_path = os.path.join(frame_folder_4, f'frame_4_{frame_number}.png')
            cv2.imwrite(frame_path, frame)
            total_frames_4 += 1

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            executor.submit(process_frame, frame_number, frame, frame_folder_4, frame_folder_60)
            frame_number += 1
            print(f"Total frames 4 saved: {total_frames_4}.\nTotal frames 60 saved: {total_frames_60}.\nTotal frames generated: {frame_number}.")
            

    base_media_path = os.path.join(settings.MEDIA_ROOT)
    frame_folder_rel = os.path.relpath(frame_folder, base_media_path)
    frame_folder_4_rel = os.path.relpath(frame_folder_4, base_media_path)
    frame_folder_60_rel = os.path.relpath(frame_folder_60, base_media_path)

    video_frames.has_frames_60 = total_frames_60 > 0
    video_frames.has_frames_4 = total_frames_4 > 0
    video_frames.total_frames_60 = total_frames_60
    video_frames.total_frames_4 = total_frames_4
    video_frames.video_frames_total = total_frames_60 + total_frames_4
    video_frames.frame_folder_path = frame_folder_rel
    video_frames.frame_folder_path_4 = frame_folder_4_rel
    video_frames.frame_folder_path_60 = frame_folder_60_rel
    video_frames.save()
    cap.release()

def annotate_frames(request, video_id, frame_type, frame_number, rank):
    video = get_object_or_404(Video, pk=video_id)
    video_frames = VideoFrames.objects.get(video=video)

    frame_type = frame_type
    frame_number = frame_number
    rank = rank

    if rank == 'Clear':
        # If rank is empty, delete the corresponding FrameAnnotations entry
        try:
            frame_annotation = FrameAnnotations.objects.get(
                video=video,
                frame_type=frame_type,
                frame_number=frame_number
            )
            frame_annotation.delete()
            return JsonResponse({'status': 'success'})
        except FrameAnnotations.DoesNotExist:
            # If the entry does not exist, return success as well
            return JsonResponse({'status': 'success'})
        except Exception as e:
            # Handle other potential exceptions (e.g., database errors) appropriately
            return HttpResponseBadRequest(f'Error: {str(e)}')
    else:
        # If rank is not empty, update or create the FrameAnnotations entry
        try:
            frame_annotation = FrameAnnotations.objects.get(
                video=video,
                frame_type=frame_type,
                frame_number=frame_number
            )

            # If the entry exists, update the rank information
            frame_annotation.rank = rank
            frame_annotation.is_annotated = True
            frame_annotation.annotator = request.user.username
            frame_annotation.save()

            return JsonResponse({'status': 'success'})
        except FrameAnnotations.DoesNotExist:
            # If the entry does not exist, create a new one
            frame_annotation = FrameAnnotations.objects.create(
                video=video,
                frame_type=frame_type,
                frame_number=frame_number,
                rank=rank,
                is_annotated=True,
                annotator=request.user.username
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            # Handle other potential exceptions (e.g., database errors) appropriately
            return HttpResponseBadRequest(f'Error: {str(e)}')