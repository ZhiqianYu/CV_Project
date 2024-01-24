# Generated by Django 5.0.1 on 2024-01-24 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('annotation', '0005_frameannotations_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotationExport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('export_name', models.CharField(default='', max_length=255)),
                ('export_time', models.DateTimeField(auto_now_add=True)),
                ('export_user', models.CharField(default='', max_length=255)),
                ('export_path', models.CharField(default='', max_length=255)),
                ('export_file_type', models.CharField(default='', max_length=255)),
                ('choosed_frames', models.ManyToManyField(to='annotation.frameannotations')),
            ],
        ),
    ]
