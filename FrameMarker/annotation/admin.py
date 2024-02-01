from django.contrib import admin
from .models import VideoFrames, FrameAnnotations

class VideoFramesAdmin(admin.ModelAdmin):
    list_display = ('video_name', 'total_frames_60', 'total_frames_4', 'video_frames_total')
    search_fields = ('video__file_name', 'has_frames_60', 'total_frames_60', 'has_frames_4', 'total_frames_4', 'video_frames_total', 'frame_folder_path', 'frame_folder_path_4', 'frame_folder_path_60')
    fields = ('video', 'has_frames_60', 'total_frames_60', 'has_frames_4', 'total_frames_4', 'video_frames_total', 'frame_folder_path', 'frame_folder_path_4', 'frame_folder_path_60')

    def video_name(self, obj):
        return obj.video.file_name

    video_name.short_description = 'Video Name'

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete() 


class FrameAnnotationsAdmin(admin.ModelAdmin):
    list_display = ('video', 'frame_type', 'frame_number', 'rank', 'is_annotated', 'annotator')
    search_fields = ('video__file_name', 'frame_type', 'frame_number', 'rank', 'is_annotated', 'annotator')
    list_filter = ('video', 'frame_type', 'frame_number', 'rank', 'is_annotated', 'annotator')

admin.site.register(VideoFrames, VideoFramesAdmin)
admin.site.register(FrameAnnotations, FrameAnnotationsAdmin)
