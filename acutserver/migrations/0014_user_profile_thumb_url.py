# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-08 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acutserver', '0013_auto_20170916_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_thumb_url',
            field=models.URLField(null=True),
        ),
    ]
