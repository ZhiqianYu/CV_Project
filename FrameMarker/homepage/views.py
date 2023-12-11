from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings

from .forms import UploadForm

import os

# 链接定向
def homepage(request):
    return render(request, 'index.html')

def videopage(request):
    return render(request, 'videos.html')

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
            return JsonResponse({'status': 'Upload Success'})
        else:
            return JsonResponse({'status': 'Upload Failed', 'message': 'Invalid form data'})
    else:
        form = UploadForm()
    return render(request, 'index.html', {'form': form})

