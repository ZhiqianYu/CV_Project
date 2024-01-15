from django.contrib import admin
from .models import VideoFrames

class VideoFramesAdmin(admin.ModelAdmin):
    list_display = ('video', 'total_frames_60', 'total_frames_4')

    def video_name(self, obj):
        return obj.video.file_name

admin.site.register(VideoFrames, VideoFramesAdmin)