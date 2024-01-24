from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from annotation.models import FrameAnnotations
from homepage.models import Video

def exportpage(request):
    return render(request, 'exportpage.html')

def exportfromannotation(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
        # 在这里处理视频信息，以及获取相关的帧标注数据
    frame_annotations = FrameAnnotations.objects.filter(video=video)


    # 在这里可以进行其他的处理，例如生成 CSV 数据等

    # 渲染 exportpage 页面
    return render(request, 'exportpage.html', {'video': video, 'frame_annotations': frame_annotations})