from django.db import models
from homepage.models import Video

class VideoFrames(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    has_frames_60 = models.BooleanField(default=False)
    has_frames_4 = models.BooleanField(default=False)
    total_frames_60 = models.IntegerField(default=0)
    total_frames_4 = models.IntegerField(default=0)
    frame_number = models.IntegerField(default=0)
    video_frames_total = models.IntegerField(default=0)
    frame_folder_path = models.CharField(max_length=255, default="") 
    frame_folder_path_4 = models.CharField(max_length=255, default="")
    frame_folder_path_60 = models.CharField(max_length=255, default="")

    def save(self, *args, **kwargs):
        self.video_frames_total = self.total_frames_60 + self.total_frames_4
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.video.file_name} - {self.total_frames_60} - {self.total_frames_4}'

    class Meta:
        verbose_name_plural = "Video Frames"

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