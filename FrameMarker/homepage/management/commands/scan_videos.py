import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from homepage.models import Video
from homepage.views import create_video
from django.conf import settings

class Command(BaseCommand):
    help = 'Scans the video directory and creates database entries for new videos.'
    
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
    
    def handle(self, *args, **options):
        username = options['username']
        video_dir = os.path.join(settings.MEDIA_ROOT, 'Video')
        try:
            admin_user = User.objects.get(username=username)
        except User.DoesNotExist:
            admin_user = User.objects.create_user('auto_scan')
            self.stdout.write(self.style.WARNING('User admin does not exist, created a new one named auto_scan'))

        # 获取数据库中所有视频条目的文件名称列表
        existing_video_file_names = list(Video.objects.values_list('file_name', flat=True))

        for filename in os.listdir(video_dir):
            file_path = os.path.join(video_dir, filename)
            # 获取视频文件名
            video_name = os.path.basename(file_path)
            file_extension = '.jpg'
            preview_file_name = os.path.splitext(video_name)[0] + file_extension
            preview_path = os.path.join(settings.MEDIA_ROOT, 'Preview', preview_file_name)
            
            os.makedirs(os.path.dirname(preview_path), exist_ok=True)

            # 检查视频文件名是否在数据库条目名称列表中
            if video_name not in existing_video_file_names and preview_file_name not in existing_video_file_names:
                create_video(file_path, preview_path, username=admin_user)
                self.stdout.write(self.style.SUCCESS(f'Successfully created Video object and Preview for {filename}'))
            else: 
                self.stdout.write(self.style.WARNING(f'Video object for {filename} already exists'))
