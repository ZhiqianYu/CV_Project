from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Video(models.Model):
    file_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    edited = models.BooleanField(default=False)
    edit_time = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        if self.edited:
            # 设置编辑时间为当前时间
            self.edit_time = datetime.now()
        else:
            # 如果未编辑，将编辑时间设为 None
            self.edit_time = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title