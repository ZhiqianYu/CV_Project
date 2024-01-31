from django.contrib import admin
from django.utils.html import format_html
from .models import Video, UserData

# Register your models here.
from .models import Video
from django.core.management import call_command

def scan_videos(modeladmin, request, queryset):
    current_user = request.user.username
    call_command('scan_videos', current_user)

scan_videos.short_description = 'Scan videos'
scan_videos.actions = None

class VideoAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'uploader', 'upload_time', 'annotation_progress', 'annotation_time', 'approved')
    readonly_fields = ('file_name', 'uploader', 'upload_time', 'annotation_time', 'preview_image', 'video_file')
    fields = ('file_name', 'upload_time', 'uploader', 'annotation_progress', 'annotation_time', 'approved', 'preview_image', 'video_file')
    actions = [scan_videos]

    def preview_image(self, obj):
        if obj.preview_file:
            return format_html('<img src="{}" style="max-height:200px; max-width:200px;"/>', obj.preview_file.url)
        else:
            return 'No Preview Available'

    preview_image.allow_tags = True
    preview_image.short_description = 'Preview'

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete() # 使用model定义的delete方法，删除文件

admin.site.register(Video, VideoAdmin)
admin.site.register(UserData)  