# Generated by Django 5.0 on 2023-12-14 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_video_preview_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='Preview/'),
        ),
    ]
