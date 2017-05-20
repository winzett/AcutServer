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


