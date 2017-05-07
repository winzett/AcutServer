from django.shortcuts import render
from django.http import HttpResponse

from .models import Post
from .models import upload_file
from .models import User
from .models import Comment
from .models import Photo_meta
from .models import Photo_info
from .models import Hash_tag
from .models import Hash_table
from .models import Comment

from django.core.urlresolvers import reverse
from .forms import upload_image_form
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from operator import eq
from django.http import JsonResponse
from boto.s3.connection import S3Connection, Bucket, Key
from django.core import serializers
import os
import boto
import boto.s3.connection
import json

##################################<redirction> redirction related functions #####################################
# Create your views here.
def jsontest(request):
  return render(request,"./jsontest.html")

def json_decoding_page(request):
  return render(request,"./json_decode.html")

@csrf_exempt
def json_decode(request):
  if 'shiny' in request.POST:
    decode_rt=request.POST['name']+", "+request.POST['hind'] 
  else:
    decode_rt="no json object or no check on the check box"
  return HttpResponse("<h1> %s </h1>" %decode_rt)

def uploadpage(request) :
  return render(request, './upload.html')

def downloadpage(request) :
  return render(request, './download.html')
#def delete_photopage(request) :
#  return render(request, './delete_photo.html')



## Main feed,comments, Good, pic info input(tag hash add, ), hash tag add, add to Hash table, tag search, challenge 

###################################<comments> comments related functions #####################################
#add5
@csrf_exempt
def get_post_comments(request):
  if request.method == 'POST':
    data = json.load(request)
    post_num = data['post_idx']
    
    cmt_set = Comment.objects.filter(post_index = post_num).order_by(comment_time)
    
    json_encode = serializers.serialize('json', cmt_set)
    
    return HttpResponse(json_encode, content_type = "application/json")

  return HttpResponse("bad access")

#add4

#add3
@csrf_exempt
def add_comment(request):
  if request.method == 'POST':
    data = json.load(request)
    u_idx = data['user_idx']
    post_num = data['post_idx']
    cmt_content = data['comment']
    
    cmt_obj = Comment(comment_content = cmt_content, post_index = post_num,
        user_index = u_idx)
    cmt_obj.save();
    return HttpResponse("success")

  return HttpResponse("bad access")
###################################################################################################


###################################<post> post related functions  #####################################
@csrf_exempt
def user_posts(request):
  if request.method == 'POST':

    data = json.load(request.POST)
    u_idx = data['user_idx']
    
    form = upload_image_form(request.POST, request.FILES)

    if form.is_valid():
      image_file = upload_file(user_index = u_idx, image = request.FILES['image'])
      image_file.save()
    else :
      return HttpResponse("image upload fail")
  
    p_img = image_file.image
    p_info = data['photo_info']
    p_long = data['longitude']
    p_la = data['latitude']
    p_content = data['content']
    hash_tags = data['hash_tags']


    #have to think about the  search speed because it wiil compare all hash
    #tags with hash tables word

    post_obj = Post(user_index = u_idx, post_img = p_img, post_content =  p_content, post_longitude = p_long, post_latitude = p_la) 
    post_obj.save()

    for info in p_info:
      has_meta = Photo_meta.objects.filter( photo_info_name = info['photo_info_name'])
    
      if has_meta.count() == 0:
        meta_obj = Photo_meta(photo_info_name = info['photo_info_name'])
        meta_obj.save()
        has_meta.refresh_from_db() 

      #photo_info_obj = Photo_info(photo_meta_index = "%s" %has_meta.photo_meta_index, photo_meta_index = "%s" %post_obj.post_index)        
      ######fixfixfixfixfixfix#########################################################################
    
    for tags in hash_tags:
      has_tag = Hash_table.objects.filter(hash_name = tags['tag_name'])

      if has_tag.count() == 0:
        table_obj = Hash_table(hash_name = tags['tag_name']) 
        table_obj.save()
        has_tag.refresh_from_db()

      hash_tag_obj = Hash_tag(hash_index = "%s" %has_tag.hash_index, post_index
          = "%s" %post_obj.post_index)


    return HttpResponse("success")
  return HttpResponse("bad access")

@csrf_exempt
def get_user_posts(request):
  if request.method == 'POST':
    #need user idx & request pic num 
    data = json.load(request)
    u_idx = data['user_idx']
    #r_num = data["request_num"]
    #send the results all first and request sequencially on client side not to
    #server side but to s3 server thumbnails(do i need to make thumbnails?) 
    #user_info = User.objects.get(user_id = u_id)
    
    posts = Post.objects.filter(user_index = u_idx).order_by('post_time')
    
    json_encode = serializers.serialize('json',posts)
    return HttpResponse(json_encode, content_type="application/json")

  return HttpResponse("bad access")

###################################################################################################




###################################<sign> sign in  and sign up #####################################

@csrf_exempt
def sign_up(request) :
  if request.method =='POST':
    data = json.load(request)
    u_id = data['user_id']  
    u_pw = data['user_pw']
    u_name = data['user_name']
    u_email = data['user_email']
    sign_up_obj = User(user_id = u_id, user_pw = u_pw, user_name = u_name,user_email = u_email, user_type = "normal",ticket = 0)
    
    sign_up_obj.save() 
    return HttpResponse("save")
    
  return HttpResponse("bad access")


@csrf_exempt
def sign_in(request):
  if request.method =='POST':
    
    json_obj = json.load(request)
    data = json_obj[0]
    
    #data = request.POST
    
    u_id = data['user_id']
    u_pw = data['user_pw']
    
    sign_in_user = User.objects.filter(user_id = u_id, user_pw =   u_pw).values('user_index','user_name','user_img','user_email','ticket')
     
    json_encode = serializers.serialize('json',sign_in_user)

    #return JsonResponse(json_encode, safe = False)
    return HttpResponse(json_encode, content_type="application/json")

  return HttpResponse("bad access")

#@csrf_exempt
#  def show_posts(request):
#    if request.method == 'POST':

###################################################################################################


###################################<upload> upload and download #####################################

@csrf_exempt
def upload(request) :
  if request.method == 'POST':
    form = upload_image_form(request.POST, request.FILES)
    
    user_obj = User.objects.filter(user_index = request.POST.get('username',False))

    if form.is_valid():
      image_file = upload_file(user_index = user_obj[0], image = request.FILES['image'])
      image_file.save()
      
      return HttpResponse("%s" %image_file.image)
  return HttpResponse("<h1>upload fail</h1>")

@csrf_exempt
def download(request) :
  cursor = connection.cursor()
  query_string = "select image from acutserver_upload_file where user_index = \"%s\"" %request.POST.get('username',False)
  cursor.execute(query_string)
  result = cursor.fetchall()
  image_url = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"
  
  if cursor.rowcount != 0 : 
    image_list = []
    result_str = ""
    
    for row in result :
      image_list.append(image_url+str(row[0]).encode('euc-kr'))  
      result_str += "<img src=\""+image_url+str(row[0])+"\">"
    
    return HttpResponse("%s" %result_str)

  return HttpResponse("<h1>download fail</h1>")


###################################################################################################

"""
@csrf_exempt
def delete_photo(request) :
  if request.method == 'POST':
    filename = request.POST.get('username',False)
  else :
    filename = 'images/2017/2/23/user/user-2017-02-23-476653.png'
     
  conn = boto.connect_s3(os.environ.get("AWS_ACCESS_KEY_ID"),os.environ.get("AWS_SECERET_ACCESS_KEY"))
    #conn = boto.connect_s3()
  b = conn.get_bucket("acut-fullsize-image")
  k = Key(b, filename)

  if k:
    return HttpResponse("<h1> %s is exist </h1>" %filename)
  else :
    return HttpResponse("<h1> delete %s fail</h1>" %filename)

  if request.method == 'POST':
    filename = request.POST.get('filename')
    conn =  S3Connection(os.environ.get("AWS_ACCESS_KEY_ID"),os.environ.get("AWS_SECERET_ACCESS_KEY"))

    b = Bucket(conn, "acut-fullsize-image")
    k = Key(b)
    k.key = filename
    b.delete_key(k)
    
    query_string = "delete from acutserver_upload_file where image=\"%s\"" %filename
    cursor.execute(query_string)
    
    return HttpResponse("<h1> delete %s success</h1>" %filename)
  #return HttpResponse("<h1> delete %s fail</h1>" %filename)
  """
