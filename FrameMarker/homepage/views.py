from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime
from django.urls import reverse


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import RegisterForm

from django.views import View

from .forms import UploadForm
from .models import Video

import os

# 链接定向
def homepage(request):
    return render(request, 'index.html')

def videopage(request):
    return render(request, 'videos.html')

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
            return redirect('login')  
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

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
            file_path = os.path.join('Video', file_name)
            destination_path = os.path.join(settings.MEDIA_ROOT, 'Video', file_name)
            
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, file_path)):
                # 文件不存在于媒体目录, 进行上传
                with open(destination_path, 'wb') as destination_file:
                    for chunk in file.chunks():
                        destination_file.write(chunk)
                
                if not Video.objects.filter(file_name=file_name).exists():
                    # 文件不存在于数据库条目中，创建新的 Video 实例并保存到数据库
                    create_video(destination_path, username)
                    return JsonResponse({'status': 'Upload Success', 'message':'Do you want to upload another file?'})
                else:
                    # 文件存在于数据库条目中
                    return JsonResponse({'status': 'Upload Success', 'message': 'Database exist file missing. File uploaded.'})
            else:
                # 文件存在于媒体目录
                if not Video.objects.filter(file_name=file_name).exists():
                    # 数据库中没有文件条目，使用 scan_videos 更新数据库
                    scan_videos(username)
                    return JsonResponse({'status': 'Upload Success', 'message': 'File exists but not in database. Rebuild database success.'})
                else:
                    # 文件存在于媒体目录且数据库中已有文件条目，不需要上传
                    return JsonResponse({'status': 'Upload Success', 'message': 'File and database exists. No need to upload.'})
        else:
            return JsonResponse({'status': 'Upload Failed', 'message': 'Invalid form data'})
    else:
        form = UploadForm()
    return render(request, 'index.html', {'form': form})


def create_video(file_path, username):
    # Get the file name
    file_name = os.path.basename(file_path)
    # 创建一个新的 Video 实例并保存到数据库
    now = datetime.now()
    title = f'{username},{now.strftime("%Y-%m-%d")},{file_name}'
    video = Video(file_name=file_name, title=title, uploader=username, upload_time=now, annotated=False, approved=False, video_file=file_path)
    video.save()

def scan_videos(username):
    video_dir = os.path.join(settings.MEDIA_ROOT, 'Video')
    existing_video_file_names = list(Video.objects.values_list('file_name', flat=True))

    # 获取媒体目录中所有文件
    all_files = os.listdir(video_dir)

    # 检查每个文件是否在数据库条目名称列表中，如果不存在，则创建数据库条目
    for filename in all_files:
        file_path = os.path.join(video_dir, filename)
        video_name = os.path.basename(file_path)

        if video_name not in existing_video_file_names:
            create_video(file_path, username)

    return JsonResponse({'status': 'Database Updated', 'message': 'All files added to the database.'})