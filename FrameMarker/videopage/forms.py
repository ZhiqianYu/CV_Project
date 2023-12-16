from django import forms
from .models import Video

class filterForm(forms.Form):
    class Meta:
        fields = ('title', 'video_file',)