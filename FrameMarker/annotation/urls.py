from django.urls import path
from . import views
from homepage import views as homepage_views
from videopage import views as videopage_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', homepage_views.introduction, name = 'introduction'),
    path('uploadpage/', homepage_views.upload, name = 'upload'),
    path('videolist/', videopage_views.video_list, name='video_list'),
    path('annotation/<int:video_id>/', views.annotation, name='annotation'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', homepage_views.register_view, name = 'register'),
    path('generate_frames/<int:video_id>/', views.generate_frames, name='generate_frames'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)