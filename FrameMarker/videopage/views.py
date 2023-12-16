from django.shortcuts import render
from homepage.models import Video

def video_list(request):
    # 获取所有视频的信息：标题、预览图、上传者和上传时间
    videos = Video.objects.all()
    return render(request, 'videos.html', {'videos': videos})