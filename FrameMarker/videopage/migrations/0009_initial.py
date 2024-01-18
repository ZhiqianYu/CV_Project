# Generated by Django 5.0.1 on 2024-01-18 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("videopage", "0008_delete_list_video"),
    ]

    operations = [
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_annotated", models.BooleanField(default=False)),
                ("upload_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
