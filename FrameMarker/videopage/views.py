from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import VideoForm
from .models import Video

def videos(request):
    # 视频页面视图函数内容...
    return render(request, 'Videos.html')

def index(request):
    return render(request, 'Videos.html')

def redirect_to_home(request):
    return redirect('index')