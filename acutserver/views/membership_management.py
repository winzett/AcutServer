from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import SimpleUploadedFile

from acutserver.form.forms import user_form
from acutserver.core.models import User
from acutserver.core.mailer import test_mail
from passlib.hash import pbkdf2_sha256

import json
import base64

@csrf_exempt
def change_user_info(request):
  if request.method == 'POST' :
    data = json.load(request)
    user_index = data['user_index']
    user_obj = User.objects.filter(index = user_index)
    if len(user_obj) == 0:
      return HttpResponse("no user")

    user_obj = user_obj[0]
    new_pw = data['pw'] if data.get('pw') else user_obj.pw
    new_nickname = data['nickname'] if data.get('nickname') else user_obj.nickname
    if data.get('img'):
      img = data['img']
      img_content = base64.b64decode(img)
      new_profile = SimpleUploadedFile('temp.jpg', img_content, getattr(img, "content_type", "application/octet-stream"))
      #request.FILES['']
    else :
      new_profile = user_obj.profile_thumb

    email = data['email'] if data.get('email') else user_obj.email
    json_obj = {'result' : []}
    try : 
      user_obj = User.objects.filter(index = user_index).update(pw = new_pw, nickname = new_nickname, profile_thumb = new_profile )
      json_obj['result'].append('1')
    except User.DoesNotExist:
      json_obj['result'].append('2')
  

  
    return HttpResponse(json.dumps(json_obj), content_type="application/json") 


  return HttpResponse("bad access")

@csrf_exempt
def send_user_info(request):

    if request.method == 'POST':
        user_index = data.json['user_index']
        
        user_obj = User.objects.filter(index =  user_index)

        return HttpResponse("success")

@csrf_exempt
def sign_up(request) :
    if request.method =='POST':
        data = json.load(request)
        #data['pw'] = pbkdf2_sha256.hash(data['pw'])
        img = data['img']
        file_convert = None
        #if data.get('profile_thumb_url') :
          #profile_thumb_url = data['profile_thumb_url']
        #else :
          #profile_thumb_url = ""
        user_last_index = User.objects.all().last().index
        if not img :
          img_content = base64.b64decode(img)
          img_result = SimpleUploadedFile('temp.jpg', img_content ,getattr(img,"content_type","application/octet-stream"))
          request.FILES[u'file'] = img_result
          file_convert = request.FILES[u'file']
       
       
        input_nickname = data['nickname'] 
        p_img = ""

        user_obj = User(user_name = data['user_name'],
                        user_id = data['user_id'],
                        pw = data['pw'],
                        nickname = input_nickname+"#"+str(user_last_index),
                        profile_thumb = file_convert
                        #profile_thumb_url = profile_thumb_url
                        )
        
        #form = user_form(data)
        #if form.is_valid :
            #form.save()
        
        user_obj.save()
        json_obj = {'result':['1']}
          
        return HttpResponse(json.dumps(json_obj), content_type='application/json')
        #else :
            ##return HttpResponse("save fail")

    return HttpResponse("bad access")


@csrf_exempt
def varifying_email(request):
    if request.method == 'POST':
        #data =json.load(request)
        #e_mail_addr = data["email"]
        e_mail_addr = request.POST.get('email')
        varifying_code = test_mail( e_mail_addr)

        return HttpResponse(varifying_code)
    return HttpResponse("bad access")


@csrf_exempt
def sign_in(request):
    if request.method =='POST':
        data = json.load(request)
        #data = json_obj
        #data = json.load(request)
        u_id = data['user_id']

        res = User.objects.filter(user_id = u_id)

        if res.exists():
            sign_in_user = res[0]
            hashed_pw = sign_in_user.pw

            if not pbkdf2_sha256.verify(data['pw'], hashed_pw):
                return HttpResponse("wrong pw")

        else :
            return HttpResponse("there is no matched id and pw")
        #user_to_json = ""+sign_in_user.as_json()
        return HttpResponse(json.dumps(sign_in_user.as_json()), content_type="application/json")

    return HttpResponse("bad access")
