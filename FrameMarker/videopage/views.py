from django.shortcuts import render
from homepage.models import Video

def homepage(request):
    return render(request, 'index.html')

def videopage(request):
    videos = Video.objects.all()  # 获取所有视频信息
    print(f"Number of videos: {len(videos)}")
    return render(request, 'videos.html', {'videos': videos})