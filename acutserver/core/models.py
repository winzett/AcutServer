from __future__ import unicode_literals
import datetime
import os
from django.utils import timezone

from django.db import models

# Create your models here.

def set_filename_format(now, instance, filename):
  return "{username}-{date}-{microsecond}{extension}".format(
    username=instance.user_id, date=str(now.date()),
    microsecond=now.microsecond, extension=os.path.splitext(filename)[1], )


def user_directory_path(instance, filename):
  now =datetime.datetime.now()
  path = "images/{year}/{month}/{day}/{username}/{filename}".format(
      year=now.year,month=now.month, day=now.day, username=instance.user_id, filename=set_filename_format(now, instance, filename), )
  return path


class User(models.Model) :
  index = models.AutoField(primary_key=True)
  user_name = models.CharField(max_length = 30, null = True);
  user_id = models.CharField(max_length=30, unique = True)
  pw = models.CharField(max_length=20)
  nickname = models.CharField(max_length=20, unique = True)
  profile_thumb = models.CharField(max_length=100, null = True)
  email = models.EmailField(null = True, db_index = True)
  user_type = models.CharField(max_length=20, default = "normal")
  vote = models.PositiveIntegerField(default=0)
  win_vote = models.PositiveIntegerField(default=0)
  my_vote = models.PositiveIntegerField(default=0)
  battle = models.PositiveIntegerField(default=0)
  win = models.PositiveIntegerField(default=0)
  state = models.BooleanField(default=True)
  last_session = models.DateTimeField()
  facebook = models.CharField(max_length=100)
  kakao = models.CharField(max_length=100)
  alarm_on = models.BooleanField(default= False)

  class Meta :
    verbose_name = "User"
    verbose_name_plural = "Users"

  def save(self, *args, **kwargs):
    self.last_session = timezone.now()
    return super(User,self).save(*args, **kwarg)

  def as_json(self):

    return dict(
        index = self.index,
        user_name = self.user_name,
        profile_thumb = self.profile_thumb,
        email = self.email,
        )
class upload_file(models.Model):
  #user = models.CharField(max_length=100, default="no user name",  null=False)
  #file_index = models.AutoField(primary_key=True)
  user_index = models.ForeignKey(User, default = '',  db_column='user_index',on_delete=models.CASCADE)
  user_id = models.CharField(max_length=30, default = '')
  image = models.ImageField(upload_to=user_directory_path,)

class Photo(models.Model) :
  index = models.AutoField(primary_key=True)
  user = models.ForeignKey(User, db_column = 'user')
  #img = models.CharField(max_length=100)
  img = models.ImageField(upload_to=user_directory_path,)
  text = models.TextField(null=True)
  victory = models.PositiveIntegerField(default=0)
  visible = models.BooleanField(default=True)
  lounge= models.BooleanField(default=True)
  new = models.BooleanField(default=True)
  upload_time = models.DateTimeField(default=timezone.now, auto_now =True)

  class Meta :
    verbose_name = "Photo"
    verbose_name_plural = "Photos"


class Battle_Log(models.Model) :
  index = models.AutoField(primary_key=True)
  p1_id = models.ForeignKey(Photo,related_name = 'p1_id')
  p2_id = models.ForeignKey(Photo, related_name = 'p2_id')
  start_time= models.DateTimeField(default=timezone.now)
  p1_vote = models.PositiveIntegerField(default = 0)
  p2_vote = models.PositiveIntegerField(default = 0)
  skip = models.PositiveIntegerField(default = 0)
  finish = models.BooleanField(default = False)




class Like_table(models.Model):
  index = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(User, db_column = 'user_id')
  battle_log_id = models.ForeignKey(Battle_Log, db_column = 'battle_log_id')
  photo_id = models.ForeignKey(Photo, db_column = 'photo_index')
  checked = models.BooleanField(default=False)
  created_at = models.DateTimeField(default = timezone.now)
  class Meta(object):
    index_together = 'user_id', 'battle_log_id', 'photo_id'
