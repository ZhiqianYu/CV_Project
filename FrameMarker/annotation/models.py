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
    frame_folder_path = models.CharField(max_length=255) 

    def save(self, *args, **kwargs):
        self.video_frames_total = self.total_frames_60 + self.total_frames_4
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.video.file_name} - {self.total_frames_60} - {self.total_frames_4}'
