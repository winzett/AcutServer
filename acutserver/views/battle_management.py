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
def show_liked_battles(request):
    if request.method == 'POST':
        data = json.load(request)
        user_obj = User.objects.filter(index = data['user_index'])

        if user_obj.count == 0 :
          return HttpResponse("no user")

        user_like_list = Like_table.objects.filter(user_id = user_obj[0]).only(battle_log_id, photo_id, checked)

        if user_like_list.count == 0 :
            return HttpResponse("no battle you like")

        user_like_battles = list()
        for like in user_like_list:
          user_like_battles.append(like.battle_log_id)

        json_str = "{ 'battles' :["
        index = 0

        img_prefix = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"
        for b in user_like_battles:
          json_str += ("{'img' : ['"+img_prefix+str(b.p1_id.img)+"', '"+img_prefix+str(b.p2_id.img)+"'], 'battle_log' : '"+str(b.index)+"'")
          json_str += ", 'likes' : "
          json_str += ("['"+str(b.p1_vote)+"','"+str(b.p2_vote)+"']}")

          if index != len(user_like_battles)-1 :
            json_str += ", "

        json_str += "]}"

        json_encode = json.dumps(json_str)

        return HttpResponse(json_encode, content_type="application/json")
    return HttpResponse("bad access")

@csrf_exempt
def show_liked_battle_results(request):
  if request.method == "POST":
    data = json.load(request)
    user_obj = User.objects.filter(index = data['user_index'])

    if user_obj.count == 0 :
      return HttpResponse("no user")

    user_like_battles = Like_table.objects.filter(user_id = user_obj[0]).only(battle_log_id, photo_id, checked)

    if user_like_battles.count == 0 :
        return HttpResponse("no battle you like")

    unchecked_list = list()
    for like in user_like_battles:
      if not like.checked:
        unchecked_list.append(like.battle_log_id)
    elif not like.battle_log_id.finish:
        unchecked_list.append(like.battle_log_id)

    if unchecked_list.count == 0 :
        return HttpResponse("no battle results")

    img_prefix = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"

    json_str = "{ 'battles' :["
    index = 0

    for b in unchecked_list:
      json_str += ("{'img' : ['"+img_prefix+str(b.p1_id.img)+"', '"+img_prefix+str(b.p2_id.img)+"'], 'battle_log' : '"+str(b.index)+"'")
      json_str += ", 'likes' : "
      json_str += ("['"+str(b.p1_vote)+"','"+str(b.p2_vote)+"']}")

      if index != len(unchecked_list)-1 :
        json_str += ", "

    json_str += "]}"

    json_encode = json.dumps(json_str)


    return HttpResponse(json_encode, content_type="application/json")

  return HttpResponse("bad access")


@csrf_exempt
def show_my_battles(request):
    if request.method == 'POST':
        data = json.load(request)
        user_obj = User.objects.filter(index = data['user_index'])

        if user_obj.count == 0 :
          return HttpResponse("no user")

        my_battles = Battle_Log.objects.filter(Q(p1 = user_obj[0]) | Q(p2 = user_obj[0]))

        if my_battles == 0 :
            return HttpResponse("no battle")

        json_str = "{ 'battles' :["
        index = 0
        img_prefix = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"
        for b in my_battles:
          json_str += ("{'img' : ['"+img_prefix+str(b.p1_id.img)+"', '"+img_prefix+str(b.p2_id.img)+"'], 'battle_log' : '"+str(b.index)+"'")
          json_str += ", 'likes' : "
          json_str += ("['"+str(b.p1_vote)+"','"+str(b.p2_vote)+"']}")

          if index != len(my_battles)-1 :
            json_str += ", "

        json_str += "]}"

        json_encode = json.dumps(json_str)


        return HttpResponse(json_encode, content_type="application/json")

    return HttpResponse("bad access")

@csrf_exempt
def show_my_battle_results(request):
  if request.method == "POST":
    data = json.load(request)
    user_obj = User.objects.filter(index = data['user_index'])

    if user_obj.count == 0 :
      return HttpResponse("no user")

    my_battles = Battle_Log.objects.filter(Q(p1 = user_obj[0]) | Q(p2 = user_obj[0]))

    if my_battles == 0 :
        return HttpResponse("no battle")


    unchecked_list = list()
    for battle in my_battles:
      if not battle.finish && user_obj[0].last_session <= battle.finish_time:
        unchecked_list.append(battle)

    if unchecked_list.count == 0 :
        return HttpResponse("no battle results")

    img_prefix = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"

    json_str = "{ 'battles' :["
    index = 0

    for b in unchecked_list:
      json_str += ("{'img' : ['"+img_prefix+str(b.p1_id.img)+"', '"+img_prefix+str(b.p2_id.img)+"'], 'battle_log' : '"+str(b.index)+"'")
      json_str += ", 'likes' : "
      json_str += ("['"+str(b.p1_vote)+"','"+str(b.p2_vote)+"']}")

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
