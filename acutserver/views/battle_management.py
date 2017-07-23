from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from acutserver.core.models import User, Battle_Log, Like_table
import json

def make_json_arr(battle):
    img_prefix = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"

    json_str = "{ 'battles' :["
    index = 0

    for b in battle:
        json_str += ("{'img' : ['"+img_prefix+str(b.p1_id.img)+"', '"+img_prefix+str(b.p2_id.img)+"'], 'battle_log' : '"+str(b.index)+"'")
        json_str += ", 'likes' : "
        json_str += ("['"+str(b.p1_vote)+"','"+str(b.p2_vote)+"']}")

        if index != len(battle)-1 :
            json_str += ", "

    json_str += "]}"

    return json.dumps(json_str)

@csrf_exempt
def show_battles(request):
    if request.method == 'POST':
        data = json.load(request)
        user_idx = data['user_index']
        user_obj = User.objects.filter(index = user_idx)

        #likes = Like_table.objects.filter(user_id = user_obj)

        battles = Battle_Log.objects.all()#.exclude(index__in = likes)

        json_encode = make_json_arr(battles)

        return HttpResponse(json_encode, content_type= "application/json")
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

        json_encode = make_json_arr(user_like_battles)

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
            elif like.battle_log_id.finish == False:
                unchecked_list.append(like.battle_log_id)

        if unchecked_list.count == 0 :
            return HttpResponse("no battle results")

        json_encode = make_json_arr(unchecked_list)


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

        json_encode = make_json_arr(my_battles)

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
            if not battle.finish and user_obj[0].last_session <= battle.finish_time:
                unchecked_list.append(battle)

        if unchecked_list.count == 0 :
            return HttpResponse("no battle results")

        json_encode = make_json_arr(unchecked_list)

        return HttpResponse(json_encode, content_type="application/json")

    return HttpResponse("bad access")

@csrf_exempt
def vote(request):
    if request.method == "POST":
        data =json.load(request)
        user_index =  data["user_index"]
        liked_photo = data["liked_photo"]
        battle_log_index = data["battle_log"]

        user_obj = User.objects.filter(index = user_index)
        if user_obj.count == 0:
            return HttpResponse("no user")
        user_obj = user_obj[0]

        battle = Battle_Log.objects.filter(index = battle_log_index)
        if battle.count == 0:
            return HttpResponse("no battle")
        battle = battle[0]

        photo = Photo.objects.filter(index = liked_photo)[0]
        if photo.count == 0:
            return HttpResponse("no photo")
        photo = photo[0]

        vote_to = battle.p1_vote if battle.p1_id.index == liked_photo else battle.p2_vote
        vote_to += 1
        battle.save

        like_log = Like_table(user_id = user_obj, battle_log_id = battle, photo_id = photo)
        like_log.save

        return HttpResponse("vote success")
    return HttpResponse("bad access")
