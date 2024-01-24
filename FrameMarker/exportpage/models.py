from django.db import models
from annotation.models import FrameAnnotations

class AnnotationExport(models.Model):
    choosed_frames = models.ManyToManyField(FrameAnnotations)
    export_name = models.CharField(max_length=255, default="")
    export_time = models.DateTimeField(auto_now_add=True)
    export_user = models.CharField(max_length=255, default="")
    export_path = models.CharField(max_length=255, default="")
    export_file_type = models.CharField(max_length=255, default="")
    
