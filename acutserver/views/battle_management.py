from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from acutserver.core.models import User, Battle_Log, Like_table, Photo
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import base64

from django.db.models import Q

import json

def make_json_arr(battle):
    img_prefix = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"

    json_str = "{ 'battles' :["
    index = 0

    for b in battle:
        json_str += "{'img' : "
        json_str += ("['"+img_prefix+str(b.p1_id.img)+"', '"+img_prefix+str(b.p2_id.img)+"'],")
        json_str += "'user_index' : "
        json_str += ("['"+str(b.p1_id.user.index)+"', '"+str(b.p2_id.user.index)+"'],")
        json_str += "'text' :"
        json_str += (" ['"+str(b.p1_id.text)+"', '"+str(b.p2_id.text)+"'],")
        json_str += "'battle_log' : "
        json_str += ("'"+str(b.index)+"',")
        json_str += "'likes' : "
        json_str += ("['"+str(b.p1_vote)+"','"+str(b.p2_vote)+"']}")

        if index != len(battle)-1 :
            json_str += ", "
        index += 1

    json_str += "]}"

    return json.dumps(json_str)

def have_battle(request):

    if request.method == 'POST':
        data = json.load(request)
        user_index = data['user_index']
        img_text = data['user_text']
        img = data['img']
        img_content = base64.b64decode(img)
        img_result = SimpleUploadedFile('temp.jpg',img_content,getattr(img, "content_type", "application/octet-stream"))

        request[u'file'] = img_result
        
        opponent_photo_index = data['opponent_photo_index']


        user_obj = User.objects.filter(index = user_index)
        if len(user_obj) == 0 :
            return HttpResponse("no user")
        
        user_obj = user_obj[0]

        photo_obj = Photo(user = user_obj, img = request[u'file'], text = img_text)

        photo_obj.save()
  

        opponent_photo_obj = Photo.objects.filter(index = opponent_photo_index)
        if len(opponent_photo_obj) == 0 :
            return HttpResponse("no photo")

        photo_obj = opponent_photo_obj[0]

        new_battle = Battle(opponent_photo_obj, photo_obj)

        new_battle.save()

        return HttpResponse("success")

    return HttpResponse("bad access")


@csrf_exempt
def show_battles(request):
    if request.method == 'POST':
        data = json.load(request)
        user_index = data['user_index']

        #likes = Like_table.objects.filter(user_id = user_obj)
        battles = Battle_Log.objects.all()#.exclude(index__in = likes)

        json_encode = make_json_arr(battles)

        return HttpResponse(json_encode, content_type= "application/json")
    return HttpResponse("bad access")



@csrf_exempt
def show_liked_battles(request):
    if request.method == 'POST':
        data = json.load(request)
        user_index = data['user_index']
        user_obj = User.objects.filter(index = user_index)

        if len(user_obj) == 0 :
            return HttpResponse("no user")
        user_obj = user_obj[0]
        user_like_list = Like_table.objects.filter(user_id = user_obj)

        if len(user_like_list) == 0 :
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
        user_index = data['user_index']
        user_obj = User.objects.filter(index = user_index)

        if len(user_obj) == 0 :
            return HttpResponse("no user")

        user_obj = user_obj[0]
        user_like_battles = Like_table.objects.filter(user_id = user_obj)

        if len(user_like_battles) == 0 :
            return HttpResponse("no battle you like")

        unchecked_list = list()
        for like in user_like_battles:
            if not like.checked:
                unchecked_list.append(like.battle_log_id)
            elif like.battle_log_id.finish == False:
                unchecked_list.append(like.battle_log_id)

        if len(unchecked_list) == 0 :
            return HttpResponse("no battle results")

        json_encode = make_json_arr(unchecked_list)


        return HttpResponse(json_encode, content_type="application/json")

    return HttpResponse("bad access")


@csrf_exempt
def show_my_battles(request):
    if request.method == 'POST':
        data = json.load(request)
        user_index = data['user_index']
        user_obj = User.objects.filter(index = user_index)

        if len(user_obj) == 0 :
            return HttpResponse("no user")

        user_obj = user_obj[0]
        photo_obj = Photo.objects.filter(user = user_obj)

        if len(photo_obj) == 0 :
            return HttpResponse("no photo")

        photo_obj = photo_obj[0]
        my_battles = Battle_Log.objects.filter((Q(p1_id = photo_obj) | Q(p2_id = photo_obj)))


        if len(my_battles) == 0 :
            return HttpResponse("no battle")

        json_encode = make_json_arr(my_battles)

        return HttpResponse(json_encode, content_type="application/json")

    return HttpResponse("bad access")

@csrf_exempt
def show_my_battle_results(request):
    if request.method == "POST":
        data = json.load(request)
        user_index = data['user_index']
        user_obj = User.objects.filter(index = user_index)

        if len(user_obj) == 0 :
            return HttpResponse("no user")

        user_obj = user_obj[0]
        photo_obj = Photo.objects.filter(user = user_obj)

        if len(photo_obj) == 0:
            return HttpResponse("no photo")

        photo_obj = photo_obj[0]

        my_battles = Battle_Log.objects.filter((Q(p1_id = photo_obj) | Q(p2_id = photo_obj)), finish = True)

        if len(my_battles) == 0 :
            return HttpResponse("no battle")


        unchecked_list = list()
        for battle in my_battles:
            if not battle.finish and user_obj.last_session <= battle.finish_time:
                unchecked_list.append(battle)

        if len(unchecked_list) == 0 :
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
        if len(user_obj) == 0:
            return HttpResponse("no user")
        user_obj = user_obj[0]

        battle = Battle_Log.objects.filter(index = battle_log_index)
        if len(battle) == 0:
            return HttpResponse("no battle")
        battle = battle[0]

        photo = Photo.objects.filter(index = liked_photo)[0]
        if len(photo) == 0:
            return HttpResponse("no photo")
        photo = photo[0]



        vote_to = battle.p1_vote if battle.p1_id.index == liked_photo else battle.p2_vote
        vote_to += 1

        voted_photo = battle.p1_id if battle.p1_id.index == liked_photo else vattle.p2_id

        voted_photo.user.my_vote += 1

        voted_photo.user.save()
        
        battle.save()

        user_obj.vote = user_obj + 1
        user_obj.save()


        like_log = Like_table(user_id = user_obj, battle_log_id = battle, photo_id = photo)
        like_log.save()

        return HttpResponse("vote success")
    return HttpResponse("bad access")
