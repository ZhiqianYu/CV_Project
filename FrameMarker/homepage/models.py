"""
    Project by @ZhiqianYu, https://github.com/ZhiqianYu and
               @DaBaivvi, https://github.com/DaBaivvi
        for the course "Computer Vision - Project" of TU Darmstadt in WS 2023-24, instructed by Yannik Frisch, Henry Krumb.
    
    Description by @Zhiqian Yu:
        This project is a web application for annotating frames of videos to prepare the data for ML.
        It is built with Django. The project is hosted on GitHub: https://github.com/ZhiqianYu/CV_Project, currently private.
        It has the basic function of registering, logging in, uploading videos, list videos, generating frames for videos,
          annotating frames, and exporting the annotations in the required formats.

        The project is divided into 4 apps: homepage, videopage, annotation, and exportpage.
        The homepage app is responsible for the introduction page, uploading videos, registering, and logging in.
        The videopage app is responsible for listing videos with ralated infos, filtering videos, and displaying the annotation progress.
        The annotation app is responsible for generating frames for videos, then annotating frames of videos.
        The exportpage app is responsible for loading the annotation data and exporting the annotations in the required formats.
    
    Introduction of this file:
        It serves as the fundamental model for the whole project. Its the base model Video, which is the parent model for all the other models.
        Including "video frames" and "annotations". Also it defines the delete and save functions for the video model. When the database is deleted,
        the corresponding file also need to be delete, this is also for the video frame model to delete the imgs.
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import os
from django.conf import settings

# 视频模型，用来储存视频信息，并放入数据库
class Video(models.Model):
    file_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    annotation_progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    annotation_time = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    video_file = models.FileField(upload_to='Video/') 
    preview_file = models.ImageField(upload_to='Preview/', null=True, blank=True)    

    def delete(self, *args, **kwargs):
        if self.video_file:
            video_file_path = self.video_file.path
            if video_file_path and os.path.exists(video_file_path):
                os.remove(video_file_path)
        
        if self.preview_file:
            preview_file_path = self.preview_file.path
            if preview_file_path and os.path.exists(preview_file_path):
                os.remove(preview_file_path)
        
        # 删除旧视频文件
        old_video_dir = os.path.join(settings.MEDIA_ROOT, 'old_Video')
        current_filename, _ = os.path.splitext(self.file_name)
        if os.path.exists(old_video_dir):
            for filename in os.listdir(old_video_dir):
                old_filename, _ = os.path.splitext(filename)
                if old_filename == current_filename:
                    old_video_path = os.path.join(old_video_dir, filename)
                    if os.path.exists(old_video_path):
                        os.remove(old_video_path)
            # 尝试删除包含旧视频文件的文件夹，如果为空的话
            try:
                os.rmdir(old_video_dir)
            except OSError:
                pass  # 如果文件夹不为空或无法删除，忽略错误
        
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

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()
    profile_pic = models.ImageField(upload_to='pic/', default='pic/default.jpg')
    subscribers = models.ManyToManyField(User, related_name='subscribers')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'User Data'
        verbose_name_plural = 'User Data'


