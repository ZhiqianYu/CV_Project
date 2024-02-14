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

from django.shortcuts import render, get_object_or_404
from homepage.models import Video
from .models import VideoFrames, FrameAnnotations
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from queue import Queue
import threading, time, os, cv2, re, shutil
from ultralytics import YOLO

model = YOLO("yolov8s.pt")

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
    if video_frames.total_frames_main_undetect is not None:
        total_frame_files = video_frames.video_frames_total
    else:
        total_frame_files = 'N/A'

    frame_paths_main = []
    frame_paths_sub = []

    # 构建 frame_paths_main 和 frame_paths_sub 列表
    if video_frames.has_frames_main or video_frames.has_frames_sub:
        media_root = settings.MEDIA_ROOT
        frame_folder_main = video_frames.frame_folder_path_main
        main_list_path = os.path.join(media_root, video_frames.frame_folder_path_main)
        frame_paths_main = [os.path.join(frame_folder_main, file) for file in os.listdir(main_list_path)]
        if video_frames.frame_folder_path_sub is not None:
            frame_folder_sub = video_frames.frame_folder_path_sub
            sub_list_path = os.path.join(media_root, video_frames.frame_folder_path_sub)
            frame_paths_sub = [os.path.join(frame_folder_sub, file) for file in os.listdir(sub_list_path)]
    else:
        frame_folder_main = False
        frame_folder_sub = False

    # 构建帧信息列表
    frame_info_list = []
    for frame_path in frame_paths_main:
        frame_number = int(frame_path.split('_')[-1].split('.')[0])
        annotation = annotations_dict.get(frame_number, None)
        if annotation is None:
            annotation = {'is_annotated': False, 'rank': ''}
        frame_info = {'frame_path': frame_path, 'frame_number': frame_number, 'annotation': annotation}
        frame_info_list.append(frame_info)

    return render(request, 'annotation.html', {'video': video, 'filename': filename, 'uploader': uploader, 
                                               'frame_paths_4': frame_paths_sub, 'frame_folder_4': frame_folder_sub,
                                               'frame_paths_60': frame_info_list, 'frame_folder_60': frame_folder_main,
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

def update_overlay(request, video_id, frame_type, frame_number):
    video = get_object_or_404(Video, pk=video_id)
    video_frames, created = VideoFrames.objects.get_or_create(video=video)

    annotations = FrameAnnotations.objects.filter(video=video)
    annotations_dict = {anno.frame_number: {'is_annotated': anno.is_annotated, 'rank': anno.rank} for anno in annotations}

    frame_info = {}
    frame_info['frame_name'] = f'frame_main_{frame_number}.jpg'
    frame_info['frame_number'] = frame_number
    frame_info['annotation'] = annotations_dict.get(frame_number, {})
    return JsonResponse({'frame_info': frame_info})

def generate_frames(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video_frames = VideoFrames.objects.filter(video=video)
    total_frames = calculate_max_frame_number(video)

    if not (video_frames.filter(has_frames_main=True).exists() and video_frames.filter(has_frames_sub=True).exists()):
        print("Frames not found or not all frames are generated. Generating frames...")
        
        try:
            # Call the separate function for frame generation
            generate_frames_for_video(video)
            return JsonResponse({'status': 'success', 'total_frames': total_frames})
        except Exception as e:
            error_message = str(e)
            print(f"Frame generation failed: {error_message}")
            return JsonResponse({'status': 'error', 'message': 'Frame generation failed', 'error': error_message}, status=500)
    else:
        print("Frames already exist and are generated.")
        return JsonResponse({'status': 'success', 'total_frames': total_frames})

def calculate_max_frame_number(video):
    video_file_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
    cap = cv2.VideoCapture(video_file_path)
    max_frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return max_frame_number

def generate_frames_for_video(video, num_threads=8):
    video_file_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
    uploadtime = video.upload_time.strftime('%Y%m%d%H%M%S') 
    filename_without_extension = os.path.splitext(video.file_name)[0]
    folder_name = f"{filename_without_extension}-{video.uploader.username}-{uploadtime}"

    frame_folder = os.path.join(settings.MEDIA_ROOT, 'Frames', folder_name)
    frame_folder_sub = os.path.join(settings.MEDIA_ROOT, 'Frames', folder_name, 'sub')
    frame_folder_main = os.path.join(settings.MEDIA_ROOT, 'Frames', folder_name, 'main')

    frame_folder_sub_tmp = os.path.join(settings.MEDIA_ROOT, frame_folder, 'temp', 'sub')
    frame_folder_main_tmp = os.path.join(settings.MEDIA_ROOT, frame_folder, 'temp', 'main')
    os.makedirs(frame_folder, exist_ok=True)
    os.makedirs(frame_folder_sub, exist_ok=True)
    os.makedirs(frame_folder_main, exist_ok=True)

    frame_number = 0
    total_frames_main_undetect = 0
    total_frames_sub_undetect = 0
    batch_size = 300
    
    try:
        def process_frame(frame_number, frame_img):
            nonlocal total_frames_main_undetect, total_frames_sub_undetect
            if frame_number % 5 == 0:
                frame_path_main_tmp = os.path.join(frame_folder_main_tmp, f'frame_main_{frame_number}.jpg')
                os.makedirs(frame_folder_main_tmp, exist_ok=True)
                cv2.imwrite(frame_path_main_tmp, frame_img)
                total_frames_main_undetect += 1

            if frame_number % 1 == 0 and frame_number % 5 != 0:
                frame_path_sub_tmp = os.path.join(frame_folder_sub_tmp, f'frame_sub_{frame_number}.jpg')
                os.makedirs(frame_folder_sub_tmp, exist_ok=True)
                cv2.imwrite(frame_path_sub_tmp, frame_img)
                total_frames_sub_undetect += 1
        
        frame_queue = Queue(maxsize=batch_size*0.25*num_threads) # Queue for storing frames to be processed, larger than batch size
        def read_and_process_frames():
            while True:
                frame_number, frame_img = frame_queue.get()  # get frame from the queue
                process_frame(frame_number, frame_img)
                frame_queue.task_done()  # tell the queue that the frame is processed

        cap = cv2.VideoCapture(video_file_path)
        # Start the threads for processing frames
        for _ in range(num_threads):
            threading.Thread(target=read_and_process_frames, daemon=True).start()

        frame_number = 0
        while True:
            # Read a batch of frames
            frames = []
            for _ in range(batch_size):
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append((frame_number, frame))
                frame_number += 1
            # put frames readed into the queue
            for frame_data in frames:
                while frame_queue.full():  # when the queue is full, wait for a short time
                    time.sleep(0.1)
                frame_queue.put(frame_data)
            if not ret:
                break
            print(f"Total frames file main saved: {total_frames_main_undetect}.\nTotal frames file sub saved: {total_frames_sub_undetect}.\nTotal frames file read: {frame_number}.")
        # Wait for all frames to be processed
        frame_queue.join()
        cap.release()
        save_frame_to_database(video, frame_folder_sub, frame_folder_main, total_frames_main_undetect, total_frames_sub_undetect)

        # detection for all frames generated
        image_paths_main_tmp = [os.path.join(frame_folder_main_tmp, file) for file in os.listdir(frame_folder_main_tmp)]
        image_paths_sub_tmp = [os.path.join(frame_folder_sub_tmp, file) for file in os.listdir(frame_folder_sub_tmp)]
        for image_path_tmp in image_paths_main_tmp + image_paths_sub_tmp:
            detection(video, frame_folder_main, frame_folder_sub, image_path_tmp)
        print(f"Detection for all frames generated done.")

    except Exception as e:
        error_message = str(e)
        print(f"Frame generation failed: {error_message}")
        return JsonResponse({'status': 'error', 'message': 'Frame generation failed', 'error': error_message}, status=500)
    
def save_frame_to_database(video, frame_folder_sub, frame_folder_main, total_frames_main_undetect, total_frames_sub_undetect):
    uploadtime = video.upload_time.strftime('%Y%m%d%H%M%S') 
    filename_without_extension = os.path.splitext(video.file_name)[0]
    folder_name = f"{filename_without_extension}-{video.uploader.username}-{uploadtime}"

    base_media_path = os.path.join(settings.MEDIA_ROOT)
    frame_folder = os.path.join(settings.MEDIA_ROOT, 'Frames', folder_name)
    frame_folder_rel = os.path.relpath(frame_folder, base_media_path)
    frame_folder_sub_rel = os.path.relpath(frame_folder_sub, base_media_path)
    frame_folder_main_rel = os.path.relpath(frame_folder_main, base_media_path)

    video_frames, _ = VideoFrames.objects.get_or_create(video=video)
    video_frames.total_frames_main_undetect = total_frames_main_undetect
    video_frames.total_frames_sub_undetect = total_frames_sub_undetect
    video_frames.video_frames_total = total_frames_main_undetect + total_frames_sub_undetect
    video_frames.frame_folder_path = frame_folder_rel
    video_frames.frame_folder_path_sub = frame_folder_sub_rel
    video_frames.frame_folder_path_main = frame_folder_main_rel
    video_frames.save()
    print(f"Databse created for video {video.file_name} with frame info.")

def updateVideoFrames(video, main_detected, sub_detected):
    video_frames, _ = VideoFrames.objects.get_or_create(video=video)
    video_frames.total_frames_main += main_detected
    video_frames.total_frames_sub += sub_detected
    video_frames.has_frames_main = video_frames.total_frames_main > 0
    video_frames.has_frames_sub = video_frames.total_frames_sub > 0
    video_frames.save()
    print(f"Databse updated for video {video.file_name} with frame info.")

def detection(video, frame_folder_main, frame_folder_sub, image_path_tmp):
    # temp folder for frames
    video_frames, created = VideoFrames.objects.get_or_create(video=video)
    frame_folder = os.path.join(settings.MEDIA_ROOT, video_frames.frame_folder_path)
    frame_folder_tmp = os.path.join(frame_folder, 'temp')
    os.makedirs(frame_folder_tmp, exist_ok=True)

    # load the image
    image = cv2.imread(image_path_tmp)
    img_name = os.path.basename(image_path_tmp)
    count_main = 0
    count_sub = 0
    # use the model to detect objects in the image
    results = model(image)
        
    def extractFrameIndexFromPath(image_path):
        match = re.search(r'_(\d+)\.jpg', image_path)
        if match:
            frame_index = int(match.group(1))
            return frame_index
        else:
            return 0
    
    # get the bounding boxes and probabilities
    for result in results:  # as result could have multiple dimensions on data, get all posible results
        box_tensor = result.boxes.xyxy.numpy() # bounding boxes of instrument tip, transformed from tensor to numpy array
        probs_tensor = result.boxes.conf.numpy() # classification probabilities, transformed from tensor to numpy 
        obj_num = result.boxes.cls.numpy() # object names

        names = {0: 'tip', 1: 'claw', 2: 'canula'}
        obj_names = [names.get(num, 'unknown') for num in obj_num]

        # see if any objects were detected
        if not box_tensor.any() or not probs_tensor.any():
            print(f'No objects detected in {img_name}')
            return False
        
        # 在原始图像上绘制边界框和标注概率
        for i in range(len(box_tensor)):
            # 获取边界框的坐标
            x1, y1, x2, y2 = box_tensor[i]
            confidence = probs_tensor[i]
            name = obj_names[i]
            if confidence > 0.5:
                # 计算文本位置
                text_loc_name = (int(x1), int(y1) - 35)
                text_loc_conf = (int(x1), int(y1) - 5)
                # 获取文本尺寸
                text_siz_name = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                text_siz_conf = cv2.getTextSize(f'{confidence:.2f}', cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                # 计算背景矩形的尺寸
                bg_siz_name = (text_siz_name[0] + 10, text_siz_name[1] + 8)
                bg_siz_conf = (text_siz_conf[0] + 10, text_siz_conf[1] + 8)
                
                # 在图像上绘制边界框
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (20, 255, 30), 2)
                # 绘制文字背景
                bg_color = (30, 50, 150)  # 背景颜色
                alpha = 0.8  # 设置透明度
                overlay = image.copy()
                cv2.rectangle(overlay, (text_loc_name[0], text_loc_name[1] - text_siz_name[1]), 
                            (text_loc_name[0] + bg_siz_name[0], text_loc_name[1]), bg_color, -1)
                cv2.rectangle(overlay, (text_loc_conf[0], text_loc_conf[1] - text_siz_conf[1]), 
                            (text_loc_conf[0] + bg_siz_conf[0], text_loc_conf[1]), bg_color, -1)
                cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
                
                # 在图像上标注对象名称和概率
                cv2.putText(image, f'{name}', text_loc_name, cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 255, 30), 2)
                cv2.putText(image, f'{confidence:.2f}', text_loc_conf, cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 255, 30), 2)

                # 保存带有边界框和标注的图像
                frame_number = extractFrameIndexFromPath(image_path_tmp)
                if frame_number % 5 == 0: # here would need to be changed if the frame number gap is not 5
                    frame_path_main = os.path.join(frame_folder_main, f'frame_main_{frame_number}.jpg')
                    cv2.imwrite(frame_path_main, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
                    count_main += 1
                else:
                    frame_path_sub = os.path.join(frame_folder_sub, f'frame_sub_{frame_number}.jpg')
                    cv2.imwrite(frame_path_sub, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
                    count_sub += 1

                print(f'{count_main} frames of main saved.\n{count_sub} frames of sub saved.\n')
                updateVideoFrames(video, count_main, count_sub)
            else:
                continue
    return True

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

    if rank == 'Delete':
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