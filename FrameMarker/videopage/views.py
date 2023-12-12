from django.shortcuts import render
from .models import VideoPreview  # 导入videopage app的视频页面模型
from homepage.models import Video  # 导入主页app的视频模型

def homepage(request):
    return render(request, 'index.html')

def videopage(request):
    return render(request, 'videos.html')

def videopage_view(request):
    videos = Video.objects.all()

    for video in videos:
        video_preview, created = VideoPreview.objects.get_or_create(video=video)
        video_preview.generate_preview()  # 生成预览图

    video_previews = VideoPreview.objects.all()

    # 渲染模板并将VideoPage对象传递给模板
    return render(request, 'videos.html', {'video_pages': video_pages})
