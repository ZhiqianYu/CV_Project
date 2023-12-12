from django.contrib import admin

# Register your models here.
from .models import Video

# 在管理界面注册视频模型， 并显示视频数量
admin.site.register(Video)