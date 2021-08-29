# Generated by Django 3.2.6 on 2021-08-29 23:30

import chat_system.models
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('chat_system', '0007_alter_story_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='story',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=0, size=[150, 150], upload_to=chat_system.models.story_upload_directory),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(crop=None, default='default.png', force_format=None, keep_meta=True, quality=0, size=[100, 100], upload_to=chat_system.models.upload_directory),
        ),
    ]
