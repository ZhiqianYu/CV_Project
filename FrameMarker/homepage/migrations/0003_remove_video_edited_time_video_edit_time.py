# Generated by Django 5.0 on 2023-12-11 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_video_edited_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='edited_time',
        ),
        migrations.AddField(
            model_name='video',
            name='edit_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
