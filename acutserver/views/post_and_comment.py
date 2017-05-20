from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import base64

import json

from acutserver.models import Post, upload_file, User, Comment, Photo_meta, Photo_info, Hash_tag, Hash_table

from acutserver.form.forms import upload_image_form


@csrf_exempt
def user_posts(request):

  if request.method == 'POST':

    data = json.load(request)
    #data = request.POST
     
    u_idx = data['user_index']
    p_info = data['photo_info']
    p_loc = data['location']
    p_content = data['content']
    img = data['img']

    img_content = base64.b64decode(img)
    img_result = SimpleUploadedFile('temp.jpg', img_content ,getattr(img,"content_type","application/octet-stream"))
    
    request.FILES[u'file'] = img_result
    
    p_img = ""
    #form = upload_image_form(request.POST, request.FILES)
    user_obj = User.objects.filter(user_index = u_idx)
    
    #if form.is_valid():
    image_file = upload_file(user_index = user_obj[0],user_id = user_obj[0].user_id, image = request.FILES[u'file'])
    try :
      image_file.save()
      p_img = image_file.image
    except Error as e :
      return HttpResponse("%s" %e.message)
    #else :
    #  return HttpResponse("is not valid")

    
  #  hash_tags = data['hash_tags']


    #have to think about the  search speed because it wiil compare all hash
    #tags with hash tables word
    
    post_obj = Post(user_index = user_obj[0], post_img = p_img, post_content = p_content, post_longitude = p_loc[0], post_latitude = p_loc[1]) 
    try :
      post_obj.save()
    except Error as e :
      return HttpResponse("%s" %e.message)

    for info in p_info:
      has_meta = Photo_meta.objects.filter( photo_info_name = info['photo_info_name'])
    
      if not has_meta.exists():
        meta_obj = Photo_meta(photo_info_name = info['photo_info_name'])
        try :
          meta_obj.save()
        except Error as e:
          return HttpResponse("%s" %e.message)

        has_meta.refresh_from_db() 
        
      photo_info_obj = Photo_info(photo_meta_index = "%s" %has_meta.photo_meta_index, info_type = info['info_type'], post_index = "%s" %post_obj.post_index) 

      try : 
        photo_info_obj.save()
      except Error as e :
        return HttpResponse("%s" %e.message)


      ######fixfixfixfixfixfix#########################################################################
    """ 
    for tags in hash_tags:
      has_tag = Hash_table.objects.filter(hash_name = tags['tag_name'])

      if not has_tag.exists():
        table_obj = Hash_table(hash_name = tags['tag_name']) 
        table_obj.save()
        has_tag.refresh_from_db()

      hash_tag_obj = Hash_tag(hash_index = "%s" %has_tag.hash_index, post_index
          = "%s" %post_obj.post_index)

    """
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
    
    #user_obj = User.objects.filter(user_index = u_idx)

    posts = Post.objects.filter(user_index = u_idx).order_by('post_time')
    
    json_encode = serializers.serialize('json',posts)
    return HttpResponse(json_encode, content_type="application/json")

  return HttpResponse("bad access")


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
    
    cmt_obj = Comment(comment_content = cmt_content, post_index = post_num, user_index = u_idx)
    
    try :
      cmt_obj.save();
    except Error as e:
      return HttpResponse("%s" %e.message)

    return HttpResponse("success")

  return HttpResponse("bad access")
