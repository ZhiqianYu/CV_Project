from django.contrib import admin
from .models import Video

# Register your models here.
from .models import Video
from django.core.management import call_command

def scan_videos(modeladmin, request, queryset):
    current_user = request.user.username
    call_command('scan_videos', current_user)

scan_videos.short_description = 'Scan videos'
scan_videos.actions = None

class VideoAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'uploader', 'upload_time', 'annotated', 'annotation_time', 'approved')
    readonly_fields = ('uploader', 'upload_time', 'annotated', 'annotation_time')
    fields = ('file_name', 'video_file', 'uploader', 'upload_time', 'annotated', 'annotation_time', 'approved')
    actions = [scan_videos]

    # 目前还有一个漏洞，这个数据库条目删除的条件是：在数据库中删除条目，并且文件实际存在，若文件不存在则删除数据库失败，
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()  # 调用模型实例的自定义 delete 方法，删除视频文件

admin.site.register(Video, VideoAdmin)