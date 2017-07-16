# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-15 08:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('acutserver', '0002_like_table_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle_log',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='photo',
            name='upload_time',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
        ),
    ]