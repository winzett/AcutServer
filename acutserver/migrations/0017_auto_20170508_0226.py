# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-07 17:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acutserver', '0016_auto_20170508_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 8, 2, 26, 48, 512354)),
        ),
    ]
