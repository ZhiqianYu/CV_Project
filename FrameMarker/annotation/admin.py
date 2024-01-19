from django.contrib import admin
from .models import VideoFrames, FrameAnnotations

class VideoFramesAdmin(admin.ModelAdmin):
    list_display = ('video_name', 'total_frames_60', 'total_frames_4', 'video_frames_total')

    def video_name(self, obj):
        return obj.video.file_name

    video_name.short_description = 'Video Name'



class FrameAnnotationsAdmin(admin.ModelAdmin):
    list_display = ('video', 'frame_type', 'frame_number', 'rank', 'is_annotated', 'annotator')
    search_fields = ('video__file_name', 'frame_type', 'frame_number', 'rank', 'is_annotated', 'annotator')
    list_filter = ('video', 'frame_type', 'frame_number', 'rank', 'is_annotated', 'annotator')

admin.site.register(VideoFrames, VideoFramesAdmin)
admin.site.register(FrameAnnotations, FrameAnnotationsAdmin)
