from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime


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
            file = form.cleaned_data['file']
            
            # Get the file name
            file_name = file.name
            
            # Set the destination path
            destination_path = os.path.join(settings.MEDIA_ROOT, 'Video', file_name)
            
            # 确保目标目录存在
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Save the file to the destination path
            with open(destination_path, 'wb') as destination_file:
                for chunk in file.chunks():
                    destination_file.write(chunk)
            
            # 检查用户是否已经登录
            if request.user.is_authenticated:
                username = request.user
            else:
                username = 'default'

            # 创建一个新的 Video 实例并保存到数据库
            now = datetime.now()
            title = f'{now.strftime("%Y-%m-%d")}_{username}_{file_name}'
            video = Video(file_name=file_name, title=title, uploader=username, upload_time=now, edited=False, approved=False)
            video.save()

            return JsonResponse({'status': 'Upload Success'})
        else:
            return JsonResponse({'status': 'Upload Failed', 'message': 'Invalid form data'})
    else:
        form = UploadForm()
    return render(request, 'index.html', {'form': form})

