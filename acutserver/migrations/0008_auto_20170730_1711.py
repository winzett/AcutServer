# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-30 08:11
from __future__ import unicode_literals

import acutserver.core.models
from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('acutserver', '0007_auto_20170723_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_thumb',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=acutserver.core.models.user_directory_path),
        ),
    ]
