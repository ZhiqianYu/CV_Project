from django.db import models
from homepage.models import Video
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_delete
import os, shutil

class VideoFrames(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    has_frames_main = models.BooleanField(default=False)
    has_frames_sub = models.BooleanField(default=False)
    total_frames_main = models.IntegerField(default=0)
    total_frames_main_undetect = models.IntegerField(default=0)
    total_frames_sub = models.IntegerField(default=0)
    total_frames_sub_undetect = models.IntegerField(default=0)
    frame_number = models.IntegerField(default=0)
    video_frames_total = models.IntegerField(default=0)
    frame_folder_path = models.CharField(max_length=255, default="") 
    frame_folder_path_sub = models.CharField(max_length=255, default="")
    frame_folder_path_main = models.CharField(max_length=255, default="")

    def delete(self, *args, **kwargs):
        # Delete associated frame images
        self.delete_frame_images()

        super().delete(*args, **kwargs)

    def delete_frame_images(self):
        # Define the paths of the frame folders
        frame_folder = os.path.join(settings.MEDIA_ROOT, self.frame_folder_path)
        frame_folder_sub = os.path.join(settings.MEDIA_ROOT, self.frame_folder_path_sub)
        frame_folder_main = os.path.join(settings.MEDIA_ROOT, self.frame_folder_path_main)

        # Delete the contents of the frame folders
        for folder_path in [frame_folder, frame_folder_sub, frame_folder_main]:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

        # Optionally, you can remove the folders themselves (if empty)
        if os.path.exists(frame_folder):
            os.rmdir(frame_folder)

        if os.path.exists(frame_folder_sub):
            os.rmdir(frame_folder_sub)

        if os.path.exists(frame_folder_main):
            os.rmdir(frame_folder_main)

    def save(self, *args, **kwargs):
        self.video_frames_total = self.total_frames_main + self.total_frames_sub
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.video.file_name} - {self.total_frames_main} - {self.total_frames_sub}'

    class Meta:
        verbose_name_plural = "Video Frames"

@receiver(pre_delete, sender=VideoFrames)
def delete_frame_images_on_video_frames_delete(sender, instance, **kwargs):
    instance.delete_frame_images()

class FrameAnnotations(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    frame_type = models.CharField(max_length=10, default="")
    frame_number = models.IntegerField(default=0)
    rank = models.CharField(max_length=20, default="")
    is_annotated = models.BooleanField(default=False)
    annotator = models.CharField(max_length=255, default="")

    def __str__(self):
        return f'{self.video.file_name} - {self.frame_type} - {self.frame_number} - {self.rank} - {self.is_annotated} - {self.annotator}' 
    
    class Meta:
        verbose_name_plural = "Frame Annotations"