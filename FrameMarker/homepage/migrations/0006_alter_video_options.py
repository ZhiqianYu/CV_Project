# Generated by Django 5.0 on 2023-12-12 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_rename_edited_video_annotated_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': 'Video', 'verbose_name_plural': 'Videos'},
        ),
    ]
