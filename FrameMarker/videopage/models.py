from django.db import models
from PIL import Image
import os
from homepage.models import Video  # 导入主页app中的视频模型

class VideoPreview(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    preview_image = models.ImageField(upload_to='VideoPreview/', blank=True)

    def generate_preview(self):
        if not self.preview_image:  # 如果预览图不存在
            video_path = self.video.video_file.path  # 主页app中视频文件路径
            preview_folder = 'VideoPreview/'  # 预览图保存的文件夹

            # 生成预览图的文件名，例如：video.mp4 -> video_preview.jpg
            preview_filename = os.path.basename(video_path).replace('.mp4', '_preview.jpg')

            preview_path = os.path.join(preview_folder, preview_filename)  # 预览图保存的完整路径

            if not os.path.exists(preview_path):  # 如果预览图文件不存在
                # 使用Pillow打开视频文件
                video_img = Image.open(video_path)
                # 计算预览图的宽高比
                width, height = video_img.size
                new_height = 100  # 设置预览图高度为100px
                new_width = int(width * (new_height / height))  # 计算宽度，保持比例
                # 生成预览图并保存
                preview_img = video_img.resize((new_width, new_height))
                preview_img.save(preview_path)

                self.preview_image = preview_path  # 将预览图路径保存到模型中
                self.save()  # 保存模型

    class Meta:
        verbose_name = 'Video Preview'
        verbose_name_plural = 'Video Previews'