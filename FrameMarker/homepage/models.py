from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models
import os   
from PIL import Image

# 视频模型，用来储存视频信息，并放入数据库
class Video(models.Model):
    file_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    annotated = models.BooleanField(default=False)
    annotation_time = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    video_file = models.FileField(upload_to='Video/') 
    preview_file = models.ImageField(upload_to='Preview/', null=True, blank=True)    

    def delete(self, *args, **kwargs):
        if self.video_file and self.video_file.path and self.preview_file and self.preview_file.path:
            os.remove(self.video_file.path)
            os.remove(self.preview_file.path)
        elif self.video_file and self.video_file.path:
            os.remove(self.video_file.path)
        elif self.preview_file and self.preview_file.path:
            os.remove(self.preview_file.path)
        pass
        super().delete(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        if not self.id:  # 如果是新创建的对象
            self.upload_time = datetime.now()  # 更新上传时间为当前时间

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
