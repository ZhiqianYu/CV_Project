import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from homepage.models import Video
from homepage.views import create_video
from django.conf import settings

class Command(BaseCommand):
    help = 'Scans the video directory and creates database entries for new videos.'

    def handle(self, *args, **options):
        video_dir = os.path.join(settings.MEDIA_ROOT, 'Video')
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            admin_user = User.objects.create_user('auto_scan', password='aut123,./')
            self.stdout.write(self.style.WARNING('User admin does not exist, created a new one named auto_scan with password aut123,./'))
        for filename in os.listdir(video_dir):
            file_path = os.path.join(video_dir, filename)
            if not Video.objects.filter(file_name=file_path).exists():
                create_video(file_path, username=admin_user)
                self.stdout.write(self.style.SUCCESS(f'Successfully created Video object for {filename}'))