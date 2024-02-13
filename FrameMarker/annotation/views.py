"""
    Project by @ZhiqianYu, https://github.com/ZhiqianYu and
               @DaBaivvi, https://github.com/DaBaivvi
        for the course "Computer Vision - Project" of TU Darmstadt in WS 2023-24, instructed by Yannik Frisch, Henry Krumb.
    
    Description by @Zhiqian Yu:
        This project is a web application for annotating frames of videos to prepare the data for ML.
        It is built with Django. The project is hosted on GitHub: https://github.com/ZhiqianYu/CV_Project, currently private.
        It has the basic function of registering, logging in, uploading videos, list videos, generating frames for videos,
          annotating frames, and exporting the annotations in the required formats.

        The project is divided into 4 apps: homepage, videopage, annotation, and exportpage.
        The homepage app is responsible for the introduction page, uploading videos, registering, and logging in.
        The videopage app is responsible for listing videos with ralated infos, filtering videos, and displaying the annotation progress.
        The annotation app is responsible for generating frames for videos, then annotating frames of videos.
        The exportpage app is responsible for loading the annotation data and exporting the annotations in the required formats.
    
    Introduction of this file:
        Important here, the way how the annotation info is stored is get the infos of the choosed frames and display it on html page, then use
        js to get the info on page and load another url with the infos. It also has some small trick to get the path and files from the files 
        loaded in html page. It relys on the file and folder name all has certain logic. Then evoke the function in the views for annotation process.
        For frame generation it's recommended to use more than 4 threads, otherwise it will cause ram overflow. As the speed of reading frame is 
        much faster than write frame img to disk.
"""

import os
import cv2
from django.shortcuts import render, get_object_or_404
from homepage.models import Video
from .models import VideoFrames, FrameAnnotations
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from concurrent.futures import ThreadPoolExecutor
from django.db.models import Count

def annotation(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video_frames, created = VideoFrames.objects.get_or_create(video=video)
    
    #frames = FrameAnnotations.objects.filter(video=video)

    annotations = FrameAnnotations.objects.filter(video=video)
    # 将数据库中的帧标注信息转换为字典，以便于后续匹配
    annotations_dict = {(anno.frame_number): anno for anno in annotations}

    filename = video.file_name
    uploader = video.uploader

    max_frame_number = calculate_max_frame_number(video)
    total_frame_files = video_frames.video_frames_total

    frame_folder_60 = video_frames.frame_folder_path_60
    frame_paths_60 = [os.path.join(frame_folder_60, f'frame_60_{i}.png') for i in range(0, max_frame_number, 5)]

    frame_folder_4 = video_frames.frame_folder_path_4
    frame_paths_4 = [os.path.join(frame_folder_4, f'frame_4_{i}.png') for i in range(0, max_frame_number, 1) if i % 5 != 0]

    # 为每张图片获取帧编号和标注信息
    frame_info_list = []
    for frame_path in frame_paths_60:
        # 从文件名中提取帧编号
        frame_number = int(frame_path.split('_')[-1].split('.')[0])
        # 从字典中获取相应帧编号的标注信息
        # 使用联接查询获取帧标注信息
        annotation = annotations_dict.get(frame_number, None)

        # 如果帧没有标注信息，为其设置一个默认值
        if annotation is None:
            annotation = {'is_annotated': False, 'rank': ''}

        # 构造帧信息字典
        frame_info = {'frame_path': frame_path, 'frame_number': frame_number, 'annotation': annotation}
        frame_info_list.append(frame_info)

    return render(request, 'annotation.html', {'video': video, 'filename': filename, 'uploader': uploader, 
                                            'frame_paths_4': frame_paths_4, 'frame_folder_4': frame_folder_4,
                                            'frame_paths_60': frame_info_list, 'frame_folder_60': frame_folder_60,
                                            'total_frame_files': total_frame_files, 'max_frame_number': max_frame_number,
                                            'annotations': annotations})

def subframe_overlay(request, video_id, frame_type, frame_number):
    # get the video object by video_id
    video = get_object_or_404(Video, pk=video_id)
    # get annotation data for subframes
    try:
        annotation = FrameAnnotations.objects.get(video=video, frame_number=frame_number, frame_type=frame_type)
        # create a dictionary to store the annotation data
        annotation_data = {
            'rank': annotation.rank,
            'is_annotated': annotation.is_annotated,
            'frame_type': annotation.frame_type,
            'frame_number': annotation.frame_number,
        }
        return JsonResponse({'annotation_data': annotation_data})
    except FrameAnnotations.DoesNotExist:
        # when data not exist return 404
        return JsonResponse({'error': 'Annotation data not found'}, status=404)

def update_overlay(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video_frames, created = VideoFrames.objects.get_or_create(video=video)

    annotations = FrameAnnotations.objects.filter(video=video)
    annotations_dict = {anno.frame_number: {'is_annotated': anno.is_annotated, 'rank': anno.rank} for anno in annotations}

    max_frame_number = calculate_max_frame_number(video)
    frame_folder_60 = video_frames.frame_folder_path_60
    frame_paths_60 = [os.path.join(frame_folder_60, f'frame_60_{i}.png') for i in range(0, max_frame_number, 5)]

    frame_info_list = []
    for frame_path in frame_paths_60:
        frame_number = int(frame_path.split('_')[-1].split('.')[0])
        annotation_data = annotations_dict.get(frame_number, {})
        frame_info = {'frame_path': frame_path, 'frame_number': frame_number, 'annotation': annotation_data}
        frame_info_list.append(frame_info)

    return JsonResponse({'frame_info_list': frame_info_list})

def generate_frames(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video_frames = VideoFrames.objects.filter(video=video)
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

def generate_frames_for_video(video, uploadtime, num_threads=8):

    video_file_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
    cap = cv2.VideoCapture(video_file_path)

    filename_without_extension = os.path.splitext(video.file_name)[0]
    folder_name = f"{filename_without_extension}-{video.uploader.username}-{uploadtime}"

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
        if frame_number % 5 == 0:
            frame_path = os.path.join(frame_folder_60, f'frame_60_{frame_number}.png')
            cv2.imwrite(frame_path, frame)
            total_frames_60 += 1

        if frame_number % 1 == 0 and frame_number % 5 != 0:
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
            print(f"Total frames sub saved: {total_frames_4}.\nTotal frames main saved: {total_frames_60}.\nTotal frames read: {frame_number}.")
            

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
    annotated_frames_count = FrameAnnotations.objects.filter(video=video).filter(is_annotated=True).count()
    
    video_frames = VideoFrames.objects.get(video=video)
    total_frames = video_frames.video_frames_total

    progress_percentage = "{:.2f}".format((annotated_frames_count / total_frames) * 100)
    video.annotation_progress = progress_percentage
    video.save()

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