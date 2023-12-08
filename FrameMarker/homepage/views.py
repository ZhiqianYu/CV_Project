from django.shortcuts import render, redirect


# Create your views here. 

def index(request):
    return render(request, 'Index.html')

def redirect_to_videos(request):
    # 重定向到 videopage 页面
    return redirect('videos')  # 这里的 'video_page' 是 videopage 中视频页面的 URL 名称
