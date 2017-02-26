from django.shortcuts import render
from django.http import HttpResponse
from .models import upload_file
from django.core.urlresolvers import reverse
from .image_form import upload_image_form
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from operator import eq
import os
import boto
import boto.s3.connection
from boto.s3.key import Key


# Create your views here.

def uploadpage(request) :
  return render(request, './upload.html')

def downloadpage(request) :
  return render(request, './download.html')

@csrf_exempt
def upload(request) :
  if request.method == 'POST':
    form = upload_image_form(request.POST, request.FILES)
    
    if form.is_valid():
      image_file = upload_file(user = request.POST.get('username',False), image = request.FILES['image'])
      image_file.save()
      #form.save()
      return HttpResponse("<h1>upload success</h1>")

  return HttpResponse("<h1>upload fail</h1>")

@csrf_exempt
def download(request) :
  cursor = connection.cursor()
  query_string = "select image from acutserver_upload_file where user = \"%s\"" %request.POST.get('username',False)
  cursor.execute(query_string)
  result = cursor.fetchall()
  #image_url =  "https://s3.ap-northeast-2.amazonaws.com/"+str(os.environ.get("AWS_STORAGE_BUCKET_NAME"))+"/"
  image_url = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"
  #return HttpResponse("<h1> %s </h1>" %result)
   # result_str = ""
   # bucket_name = 'acut-fullsize-image'i
   # conn = boto.connect_s3(
   #     aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
   #     aws_secret_access_key =  = os.environ.get("AWS_SECRET_ACCESS_KEY"),
   #     host = 's3.ap-northeast-2.amazonaws.com',
   #     calling_format = boto.s3.connection.OrdinaryCallingFormat()

   #    )
   # bucket = conn.get_bucket(bucket_name)
  if cursor.rowcount != 0 : 
    image_list = []
    result_str = ""
    
    for row in result :

      image_list.append(image_url+str(row).encode('euc-kr'))  
      #key = Key(bucket, row)
      
      result_str += image_url+str(row)

    
    return HttpResponse("<h1> %s </h1>" %result_str)

  return HttpResponse("<h1>download fail</h1>")
