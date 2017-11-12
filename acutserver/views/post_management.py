# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from acutserver.core.models import User,Post

import base64
import sys
import json

@csrf_exempt
def create(request):
  if request.method == 'POST':
    data = json.load(request)

    user_index = data.get('user_index')
    post_title = data.get('post_title')
    post_body = data.get('post_body')
    post_img = data.get('post_img')

    json_obj = {'result': []}
    
    if not user_index or not post_title or not post_body:
      json_obj['result'].append(0)
      return HttpResponse(json.dumps(json_obj), content_type="application/json")
    

    
    user_obj = User.objects.filter(index = user_index)

    if len(user_obj) == 0:
      json_obj['result'].append(0)
      return HttpResponse(json.dumps(json_obj), content_type="application/json")
    else :
      user_obj = user_obj[0]

    new_post = Post(user = user_obj, title = post_title, body = post_body)

    new_post.save()
      
    json_obj['result'].append(1)


    return HttpResponse(json.dumps(json_obj), content_type="application/json")

  return HttpResponse("bad access")

@csrf_exempt
def edit(request):
  if request.method == 'POST':
    data = json.load(request)
    post_index = data.get('post_index')
    user_index = data.get('user_index')
    post_title = data.get('post_title')
    post_body = data.get('post_body')
    post_img = data.get('post_img')

    json_obj = {'result': []}
    
    if not post_index or not user_index or not post_title or not post_body:
      json_obj['result'].append(0)
      return HttpResponse(json.dumps(json_obj), content_type="application/json")
    

    
    user_obj = User.objects.filter(index = user_index)
    
    if len(user_obj) == 0:
      json_obj['result'].append(0)
      return HttpResponse(json.dumps(json_obj), content_type="application/json")
    else :
      user_obj = user_obj[0]

    try :
      Post.objects.filter(user = user_obj, index = post_index).update(title = post_title, body = post_body)
      json_obj['result'].append(1)
    except Post.DoesNotExist:
      json_obj['result'].append(0)


    return HttpResponse(json.dumps(json_obj), content_type="application/json")

  return HttpResponse("bad access")

@csrf_exempt
def delete(request):
  if request.method == 'POST':
    data = json.load(request)
    user_index = data.get('user_index')
    post_index = data.get('post_index')

    json_obj = {'result': []}
    
    if not user_index or not post_index:
      json_obj['result'].append(0)
      return HttpResponse(json.dumps(json_obj), content_type="application/json")
    

    
    user_obj = User.objects.filter(index = user_index)

    if len(user_obj) == 0:
      json_obj['result'].append(0)
      return HttpResponse(json.dumps(json_obj), content_type="application/json")
    else :
      user_obj = user_obj[0]


    try:
      Post.objects.filter(index = post_index, user = user_obj).delete()
      json_obj['result'].append(1)
    except Post.DoesNotExist:
      json_obj['result'].append(0)

    return HttpResponse(json.dumps(json_obj), content_type="application/json")

  return HttpResponse("bad access")

@csrf_exempt
def show(request, post_index):
  #post_index = data.get('post_index')

  json_obj = {'result': []}
    
  if not post_index:
    json_obj['result'].append(0)
    return HttpResponse(json.dumps(json_obj), content_type="application/json")
    

  try:
    post_obj = Post.objects.get(index = post_index )
    json_obj['result'].append(1)
    json_obj['post'] = {'post_index': post_obj.index, 'title': post_obj.title, 'user_index': post_obj.user.index, 'user_nickname': post_obj.user.nickname, 'body': post_obj.body}
  except Post.DoesNotExist:
    json_obj['result'].append(0)


  return HttpResponse(json.dumps(json_obj), content_type="application/json")


@csrf_exempt
def index(request):


  json_obj = {'result': []}
    

  try:
    post_list = Post.objects.all().order_by('-created_at')
    json_obj['result'].append(1)
    json_obj['posts'] = []
      
    for post in post_list :
      json_obj['posts'].append({'post_index': post.index, 'title': post.title, 'user_index': post.user.index, 'user_nickname': post.user.nickname, 'body': post.body})

  except Post.DoesNotExist:
    json_obj['result'].append(0)


  return HttpResponse(json.dumps(json_obj), content_type="application/json")

