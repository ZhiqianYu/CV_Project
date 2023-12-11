from django.shortcuts import render

def homepage(request):
    return render(request, 'index.html')

def videopage(request):
    return render(request, 'videos.html')