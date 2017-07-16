from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from acutserver.core.models import User, Battle_Log, Like_table
import json

@csrf_exempt
def show_battles(request):
  if request.method == 'POST':
    data = json.load(request)
    user_idx = data['user_index']
    user_obj = User.objects.filter(index = user_idx)
    
    #likes = Like_table.objects.filter(user_id = user_obj)
    

    battles = Battle_Log.objects.all()#.exclude(index__in = likes)
    
    img_prefix = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"

    json_str = "{ 'battles' :["
    index = 0

    for b in battles:
      json_str += ("{'img' : ['"+img_prefix+str(b.p1_id.img)+"', '"+img_prefix+str(b.p2_id.img)+"'], 'battle_log' : '"+str(b.index)+"', 'likes' : ["+str(b.p1_vote)+", "+str(b.p2_vote)+"]}")
      
      if index != len(battles)-1 :
        json_str += ", "

      index += 1;

    
    json_str += "]}"

    json_encode = json.dumps(json_str)

    return HttpResponse(json_encode, content_type= "application/json")
  return HttpResponse("bad access")

@csrf_exempt
def add_like(request):
  return HttpResponse("bad access")

@csrf_exempt
def show_battle_results(request):
  if request.method == "POST":
    data = json.load(request)
    user_obj = User.objects.filter(index = data['user_index'])

    if user_obj.count == 0 :
      return HttpResponse("no user")
    
    user_like_battles = Like_table.objects.filter(user_id = user_obj[0]).only(battle_log_id, photo_id, checked)
    unchecked_list = list()
    for battle in user_like_battles:
      if not battle.checked:
        unchecked_list.append(battle.battle_log_id) 
      
 
    
    img_prefix = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"

    json_str = "{ 'battles' :["
    index = 0

    for b in unchecked_list:
      json_str += ("{'img' : ['"+img_prefix+str(b.p1_id.img)+"', '"+img_prefix+str(b.p2_id.img)+"'], 'battle_log' : '"+str(b.index)+"'")

      
      json_str += " 'likes' : ["
      json_str += ("{'"+b.battle_log_id.p1_vote+"','"+b.battle_log_id.p2_vote+"']}")
      if index != len(unchecked_list)-1 :
        json_str += ", "

    
    json_str += "]}"

    json_encode = json.dumps(json_str)


    return HttpResponse(json_encode, content_type="application/json")

  return HttpResponse("bad access")


@csrf_exempt
def vote(request):
  if request.method == "POST":
    data =json.load(request)
    user_obj = User.objects.filter(index = data["user_index"])
    
    if user_obj.count == 0:
      return HttpResponse("no user")




  return HttpResponse("bad access")
