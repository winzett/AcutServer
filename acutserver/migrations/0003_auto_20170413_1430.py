# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 05:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acutserver', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge_comment',
            fields=[
                ('ch_comment_index', models.AutoField(primary_key=True, serialize=False)),
                ('ch_comment_content', models.TextField(null=True)),
                ('ch_comment_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Challenger',
            fields=[
                ('ch_index', models.AutoField(primary_key=True, serialize=False)),
                ('ch_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_index', models.AutoField(primary_key=True, serialize=False)),
                ('comment_content', models.TextField(null=True)),
                ('comment_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('follow_index', models.AutoField(primary_key=True, serialize=False)),
                ('follower_user_index', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower_user_index', to='acutserver.User')),
                ('following_user_index', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following_user_index', to='acutserver.User')),
            ],
        ),
        migrations.CreateModel(
            name='Hash_table',
            fields=[
                ('hash_index', models.AutoField(primary_key=True, serialize=False)),
                ('hash_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hash_tag',
            fields=[
                ('hash_tag_index', models.AutoField(primary_key=True, serialize=False)),
                ('hash_index', models.ForeignKey(db_column='hash_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.Hash_table')),
            ],
        ),
        migrations.CreateModel(
            name='Like_table',
            fields=[
                ('like_index', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Photo_info',
            fields=[
                ('photo_info_index', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Photo_meta',
            fields=[
                ('photo_meta_index', models.AutoField(primary_key=True, serialize=False)),
                ('photo_info_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_index', models.AutoField(primary_key=True, serialize=False)),
                ('post_img', models.CharField(max_length=100)),
                ('post_content', models.TextField(null=True)),
                ('post_like', models.PositiveIntegerField(default=0)),
                ('challenge', models.BooleanField(default=False)),
                ('champion', models.BooleanField(default=False)),
                ('user_index', models.ForeignKey(db_column='user_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.User')),
            ],
        ),
        migrations.AddField(
            model_name='photo_info',
            name='photo_meta_index',
            field=models.ForeignKey(db_column='photo_meta_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.Photo_meta'),
        ),
        migrations.AddField(
            model_name='photo_info',
            name='post_index',
            field=models.ForeignKey(db_column='post_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.Post'),
        ),
        migrations.AddField(
            model_name='like_table',
            name='post_index',
            field=models.ForeignKey(db_column='post_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.Post'),
        ),
        migrations.AddField(
            model_name='like_table',
            name='user_index',
            field=models.ForeignKey(db_column='user_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.User'),
        ),
        migrations.AddField(
            model_name='hash_tag',
            name='post_index',
            field=models.ForeignKey(db_column='post_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post_index',
            field=models.ForeignKey(db_column='post_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_index',
            field=models.ForeignKey(db_column='user_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.User'),
        ),
        migrations.AddField(
            model_name='challenger',
            name='ch1_post_index',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ch1_post_index', to='acutserver.Post'),
        ),
        migrations.AddField(
            model_name='challenger',
            name='ch2_post_index',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ch2_post_index', to='acutserver.Post'),
        ),
        migrations.AddField(
            model_name='challenge_comment',
            name='post_index',
            field=models.ForeignKey(db_column='post_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.Post'),
        ),
        migrations.AddField(
            model_name='challenge_comment',
            name='user_index',
            field=models.ForeignKey(db_column='user_index', on_delete=django.db.models.deletion.CASCADE, to='acutserver.User'),
        ),
    ]
