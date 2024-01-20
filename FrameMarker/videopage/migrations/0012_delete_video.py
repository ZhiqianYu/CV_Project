from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videopage', '0011_alter_video_options_video_homepage_video'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Video',
        ),
    ]
