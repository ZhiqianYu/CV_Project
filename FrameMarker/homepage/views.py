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
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_authenticated:  # 检查用户是否已登录
                username = request.user
            else:
                username = 'default'

            file = form.cleaned_data['file']
            file_name = file.name
            video_path = os.path.join(settings.MEDIA_ROOT, 'Video', file_name)

            file_extension = '.jpg'
            preview_file_name = os.path.splitext(file_name)[0] + file_extension
            preview_path = os.path.join(settings.MEDIA_ROOT, 'Preview', preview_file_name)
            
            os.makedirs(os.path.dirname(video_path), exist_ok=True)
            os.makedirs(os.path.dirname(preview_path), exist_ok=True)

            video_exists = os.path.exists(video_path)
            preview_exists = os.path.exists(preview_path)
            database_exists = Video.objects.filter(file_name=file_name).exists()

            if not video_exists:
                if not preview_exists:
                    if not database_exists:
                        # 文件不存在，预览图不存在，数据库不存在
                        # 文件不存在，预览图不存在，数据库不存在
                        with open(video_path, 'wb') as destination_file:
                            for chunk in file.chunks():
                                destination_file.write(chunk)
                        video_path = video_format_transform(video_path)
                        generate_preview(video_path, preview_path)
                        create_video(video_path, preview_path, username)
                        return JsonResponse({'status': 'Upload Success', 'message': 'File uploaded. Database and preview created.'})
                    else:
                        # 文件不存在，预览图不存在，数据库存在
                        with open(video_path, 'wb') as destination_file:
                            for chunk in file.chunks():
                                destination_file.write(chunk)
                        video_path = video_format_transform(video_path)
                        generate_preview(video_path, preview_path)
                        Video.objects.filter(file_name=file_name).update(video_file=video_path, preview_file=preview_path)
                        return JsonResponse({'status': 'Upload Success', 'message': 'File uploaded, database updated, preview created.'})
                else:
                    if not database_exists:
                        # 文件不存在，预览图存在，数据库不存在
                        with open(video_path, 'wb') as destination_file:
                            for chunk in file.chunks():
                                destination_file.write(chunk)
                        video_path = video_format_transform(video_path)
                        create_video(video_path, preview_path, username)
                        return JsonResponse({'status': 'Upload Success', 'message': 'File uploaded. Database created.'})
                    else:
                        # 文件不存在，预览图存在，数据库存在
                        with open(video_path, 'wb') as destination_file:
                            for chunk in file.chunks():
                                destination_file.write(chunk)
                        video_path = video_format_transform(video_path)
                        Video.objects.filter(file_name=file_name).update(video_file=video_path, preview_file=preview_path)
                        return JsonResponse({'status': 'Upload Success', 'message': 'File uploaded, database updated.'})
            else:
                if not preview_exists:
                    if not database_exists:
                        # 文件存在，预览图不存在，数据库不存在
                        generate_preview(video_path, preview_path)
                        create_video(video_path, preview_path, username)
                        return JsonResponse({'status': 'Upload Success', 'message': 'File exist, database and preview created.'})
                    else:
                        # 文件存在，预览图不存在，数据库存在
                        generate_preview(video_path, preview_path)
                        Video.objects.filter(file_name=file_name).update(video_file=video_path, preview_file=preview_path)
                        return JsonResponse({'status': 'Upload Success', 'message': 'File exist, database updated, preview created.'})
                else:
                    if not database_exists:
                        # 文件存在，预览图存在，数据库不存在
                        create_video(video_path, preview_path, username)
                        return JsonResponse({'status': 'Upload Success', 'message': 'Files exist, database created'})
                    else:
                        # 文件存在，预览图存在，数据库存在
                        Video.objects.filter(file_name=file_name).update(video_file=video_path, preview_file=preview_path)
                        return JsonResponse({'status': 'Upload Success', 'message': 'Files exist, database updated.'})
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
    # 转换视频格式
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
