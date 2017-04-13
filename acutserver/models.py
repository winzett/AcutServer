from __future__ import unicode_literals
import datetime
import os

from django.db import models

# Create your models here.

def set_filename_format(now, instance, filename): 
  return "{username}-{date}-{microsecond}{extension}".format(
    username=instance.user, date=str(now.date()),
    microsecond=now.microsecond, extension=os.path.splitext(filename)[1], ) 
  

def user_directory_path(instance, filename):
  now =datetime.datetime.now()
  path = "images/{year}/{month}/{day}/{username}/{filename}".format(
      year=now.year,month=now.month, day=now.day, username=instance.user, filename=set_filename_format(now, instance, filename), )
  return path 

class upload_file(models.Model):
   user = models.CharField(max_length=100, default="no user name",  null=False)
   image = models.ImageField(
       upload_to=user_directory_path,
       )

class User(models.Model) :
  user_index = models.AutoField(primary_key=True)
  user_id = models.CharField(max_length=30)
  user_pw = models.CharField(max_length=20)
  user_name = models.CharField(max_length=20)
  user_img = models.CharField(max_length=100, null = True)
  user_email = models.EmailField()
  user_type = models.CharField(max_length=20)
  ticket = models.PositiveIntegerField(default=0)

class Post(models.Model) :
  post_index = models.AutoField(primary_key=True)
  user_index = ForeignKey(User, db_column = 'user_index', on_delete=models.CASCADE)
  post_img = models.CharField(max_length=100)
  post_content = models.TextField(null=True)
  post_like = models.PositiveInteger(default=0)
  challenge = models.BooleanField(default=False)
  champion = models.BooleanField(default=False)

class Challenger(models.Model) :
  ch_index = models.AutoField(primary_key=True)
  ch1_post_index = ForeignKey(Post, db_column = 'ch1_post_index',on_delete=models.CASCADE)
  ch2_post_index = ForeignKey(Post, db_column = 'ch2_post_index',on_delete=models.CASCADE)
  ch_time = models.DateTimeField(auto_now_add=True, auto_now= True)

class Hash_table(models.Model) :
  hash_index = models.AutoField(primary_key=True)
  hash_name = models.CharField(max_length=100)

class Comment(models.Model):
  comment_index  = models.AutoField(primary_key=True)
  post_index = ForeignKey(Post, db_column = 'post_index',on_delete=models.CASCADE)
  user_index = ForeignKey(User, db_column = 'user_index',on_delete=models.CASCADE)
  comment_content = models.TextField(null=True)
  comment_time = models.DateTimeField_(auto_now_add=True, auto_now=True)

class Like_table(models.Model):
  like_index = models.AutoField(primary_key=True)
  user_index = ForeignKey(User, db_column = 'user_index',
      on_delete=models.CASCADE)
  post_index = ForeignKey(Post, db_column = 'post_index',
      on_delete=models.CASCADE)

class Follow (models.Model):
  follow_index = models.AutoField(primary_key=True)
  following_user_index = ForeignKey(User, db_column = 'user_index',
      on_delete=models.CASCADE)
  follower_user_index = ForeignKey(User, db_column = 'user_index',
      on_delete=models.CASCADE)


class Hash_tag(models.Model) :
  hash_tag_index = models.AutoField(primary_key=True)
  post_index = ForeignKey(Post, db_column = 'post_index',
      on_delete=models.CASCADE)
  hash_index = ForeignKey(Hash_table, db_column = 'hash_index',
      on_delete=models.CASCADE)

class Challenge_comment (models.Model) :
  ch_comment_index  = models.AutoField(primary_key=True)
  post_index = ForeignKey(Post, db_column = 'post_index',
      on_delete=models.CASCADE)
  user_index = ForeignKey(User, db_column = 'user_index',
      on_delete=models.CASCADE)
  ch_comment_content = models.TextField(null=True)
  ch_comment_time = models.DateTimeField(auto_now_add=True, auto_now=True)

class Photo_meta(models.Model) :
  photo_meta_index = models.AutoField(primary_key=True)
  photo_info_name = models.CharField(max_length = 50)

class Photo_info (models.Model):
  photo_info_index = models.AutoField(primary_key=True)
  post_index = ForeignKey(Post, db_column = 'post_index',
      on_delete=models.CASCADE)
  photo_meta_index = ForeignKey(Photo_meta, db_column = 'photo_meta_index',
      on_delete=models.CASCADE)



