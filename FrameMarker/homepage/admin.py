from django.contrib import admin

# Register your models here.
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_Video_count')

    def get_Video_count(self, obj):
        return Video.objects.count()

    get_Video_count.short_description = 'Video Count'

admin.site.register(Video, VideoAdmin)