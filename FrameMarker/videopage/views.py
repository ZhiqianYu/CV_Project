from django.shortcuts import render
from homepage.models import Video 

def homepage(request):
    return render(request, 'index.html')

def videopage(request):
    return render(request, 'videos.html')

def videopage_view(request):
    return render(request, 'videos.html')
