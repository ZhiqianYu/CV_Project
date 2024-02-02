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
        This file is the homepage views.py. The main functions defined here are: register and login of user. How to process the uploaded video.
        For video upload, it need to check the database and media resources whether the video is already exist or not. Then it will create the
        video file in the media fold and generate a preview img for the video. Finally, it will create a database entry for the video.
        If the uploaded video is not MP4, which is the required format for video player in annotation page, it will convert the video to MP4 format.
        And store the original video in the old_Video folder. Then treat the new MP4 file as a new uploaded video. To generate preview 
        and create database entry.
        It also has a scan video function, it serves as to check the database and media resources whether there are existing files which is not
        present in the database, it's a function in the admin page of videos. It will create or update database entry for the existing files.  
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from .forms import RegisterForm, UploadForm
from .models import Video
import os
import cv2
import ffmpeg
from concurrent.futures import ThreadPoolExecutor
from django.contrib.auth.decorators import login_required
from PIL import Image

# 链接定向
def introduction(request):
    return render(request, 'introduction.html')

def upload(request):
    return render(request, 'upload.html')

# 用户注册
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            # 创建新用户并保存到数据库
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            # 注册成功后重定向到某个页面，比如登录页面
            messages.success(request, 'Account has been created successfully.')
            return JsonResponse({'status': 'success', 'username': username})  
        else:
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error', 'errors': errors})  
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

# Login
def login_user(request):
     if not request.user.is_authenticated:
         if request.method == 'POST':
             username = request.POST['username']
             password = request.POST['password']
             check_user = authenticate(username = username, password = password)
             if check_user is not None:
                 login(request, check_user)
                 return redirect('introduction')
             else:
                 messages.waring(request, 'Invalid Username or Password.')
                 return redirect('register')
         return redirect('introduction')
     else:
         return redirect('introduction')

#Logout
def logout_user(request):
    request.session.flush()
    logout(request)
    return redirect('introduction')

#Search
def search(request):
    query = request.GET.get('search_query', '')

    video_results = Video.objects.filter(title__icontains=query)
    user_results = UserData.objects.filter(user__username__icontains=query)

    params = {'query': query, 'video_results': video_results, 'user_results': user_results}

    return render(request, 'introduction.html', params)

# 文件上传Form
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            username = request.user
            file = form.cleaned_data['file']
            file_name = file.name

            video_path = os.path.join(settings.MEDIA_ROOT, 'Video', file_name)
            preview_path = os.path.join(settings.MEDIA_ROOT, 'Preview', os.path.splitext(file_name)[0] + '.jpg')

            os.makedirs(os.path.dirname(video_path), exist_ok=True)
            os.makedirs(os.path.dirname(preview_path), exist_ok=True)

            video_exists = os.path.exists(video_path)
            preview_exists = os.path.exists(preview_path)
            database_exists = Video.objects.filter(file_name=file_name).exists()

            if not video_exists:
                with open(video_path, 'wb') as destination_file:
                    for chunk in file.chunks():
                        destination_file.write(chunk)

                video_path = video_format_transform(video_path)
                generate_preview(video_path, preview_path)

                if database_exists:
                    Video.objects.filter(file_name=file_name).update(video_file=video_path, preview_file=preview_path)
                    message = 'File uploaded, database updated, preview created.'
                else:
                    create_video(video_path, preview_path, username)
                    message = 'File uploaded, database and preview created.'

            else:
                if not preview_exists:
                    generate_preview(video_path, preview_path)

                if database_exists:
                    Video.objects.filter(file_name=file_name).update(video_file=video_path, preview_file=preview_path)
                    message = 'File exists, database updated, preview created.'
                else:
                    create_video(video_path, preview_path, username)
                    message = 'File exists, database and preview created.'

            messages.success(request, message)
            return JsonResponse({'status': 'Upload Success', 'message': message})

        else:
            return JsonResponse({'status': 'Upload Failed', 'message': 'Invalid form data'})

    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})

# 数据库操作
def create_video(video_path, preview_path, username):
    now = datetime.now()

    file_name = os.path.basename(video_path)
    title = f'{username},{now},{file_name}'

    base_media_path = os.path.join(settings.MEDIA_ROOT)

    video_path = os.path.relpath(video_path, base_media_path)
    preview_path = os.path.relpath(preview_path, base_media_path)

    video = Video(file_name=file_name, title=title, uploader=username, upload_time=now, annotation_progress=0, approved=False, video_file=video_path, preview_file=preview_path)
    video.save()

def video_format_transform(video_path):
    file_name = os.path.basename(video_path)
    file_extension = os.path.splitext(file_name)[1]
    if file_extension != '.mp4':
        new_file_name = os.path.splitext(file_name)[0] + '.mp4'
        new_video_path = os.path.join(settings.MEDIA_ROOT, 'Video', new_file_name)
        print ('New File Name is:', new_file_name)
        print ('New Video Path is:', new_video_path)
        
        try:
            ffmpeg.input(video_path).output(new_video_path).run()
            print('Video format converted.')
            print ('New File Name is:', new_file_name)
            print ('New Video Path is:', new_video_path)
        except ffmpeg.Error as e:
            print(f'Error during ffmpeg conversion: {e.stderr}')
            return video_path

        # 移动原始文件到old_Video目录
        old_video_dir = os.path.join(settings.MEDIA_ROOT, 'old_Video')
        os.makedirs(old_video_dir, exist_ok=True)
        old_video_path = os.path.join(old_video_dir, file_name)
        os.rename(video_path, old_video_path)
        return new_video_path
    else:
        return video_path
    

def generate_preview(video_path, preview_path):
    # 生成预览图
    video = cv2.VideoCapture(video_path)
    success, frame = video.read()

    while success and cv2.mean(frame)[0] < 30:
        # 跳过纯黑帧
        success, frame = video.read()

    if success:
        width = 320
        height = int(frame.shape[0] * (width / frame.shape[1]))  # 按比例调整高度
        frame = cv2.resize(frame, (width, height))
        # 转换为RGB图像
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 创建PIL图像对象
        image = Image.fromarray(frame)
        # 保存预览图
        image.save(preview_path)
    video.release()

def scan_videos(username):
    video_dir = os.path.join(settings.MEDIA_ROOT, 'Video')
    existing_video_file_names = list(Video.objects.values_list('file_name', flat=True))

    # 获取媒体目录中所有文件
    all_files = os.listdir(video_dir)

    # 检查每个文件是否在数据库条目名称列表中，如果不存在，则创建数据库条目
    for filename in all_files:
        file_path = os.path.join(video_dir, filename)
        preview_path = os.path.join(settings.MEDIA_ROOT, 'Preview', filename)
        video_name = os.path.basename(file_path)

        if video_name not in existing_video_file_names:
            create_video(file_path, preview_path, username)

    return JsonResponse({'status': 'Database Updated', 'message': 'All files added to the database.'})
