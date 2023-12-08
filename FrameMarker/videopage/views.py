from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import VideoForm
from .models import Video

def upload_video(request):
       if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
               form.save()
               return redirect('video_list')  # Redirect to video list page
       else:
           form = VideoForm()
           return render(request, 'upload_video.html', {'form': form})
 
def video_list(request):
     videos = Video.objects.all()
     return render(request, 'video_list.html', {'videos': videos})

def index(request):
    return render(request, 'Videos.html')