from django.contrib import admin
from .models import VideoFrames

class VideoFramesAdmin(admin.ModelAdmin):
    list_display = ('video_name', 'total_frames_60', 'total_frames_4', 'video_frames_total')

    def video_name(self, obj):
        return obj.video.file_name

    video_name.short_description = 'Video Name'

admin.site.register(VideoFrames, VideoFramesAdmin)
