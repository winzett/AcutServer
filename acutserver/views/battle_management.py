from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from acutserver.core.models import User, Battle_Log, Like_table, Photo
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import base64

from django.db.models import Q
from django.core import serializers
import json

def make_json_arr(battles):
    img_prefix = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"

    json_arr = {'battles' : []} # 'battles' :
    index = 0
    
    if len(battles) > 1:
      for b in battles:


        json_obj = {
            'img' : [ img_prefix+str(b.p1_id.img), img_prefix+str(b.p2_id.img)],
            'user_index' : [str(b.p1_id.user.index) , str(b.p2_id.user.index)],
            'user_profile' : [img_prefix+str(b.p1_id.user.profile_thumb), img_prefix+str(b.p2_id.user.profile_thumb)],
            'text' : [ b.p1_id.text, b.p2_id.text ],
            'photo_index' : [b.p1_id.index, b.p2_id.index],
            'battle_log' : str(b.index),
            'liked_photo' : [],
            'likes' : [ str(b.p1_vote), str(b.p2_vote) ],
        }

        json_arr['battles'].append(json_obj)

    else :
      if not battles is None: 
        b = battles[0]
        json_obj = {
            'img' : [ img_prefix+str(b.p1_id.img), img_prefix+str(b.p2_id.img)],
            'user_index' : [str(b.p1_id.user.index) , str(b.p2_id.user.index)],
            'user_profile' : [img_prefix + str(b.p1_id.user.profile_thumb), img_prefix + str(b.p2_id.user.profile_thumb)],
            'text' : [ b.p1_id.text, b.p2_id.text ],
            'photo_index' : [b.p1_id.index, b.p2_id.index],
            'battle_log' : str(b.index),
            'likes' : [ str(b.p1_vote), str(b.p2_vote) ],
        }

        json_arr['battles'].append(json_obj)


    return json.dumps(json_arr)



@csrf_exempt
def have_battle(request):

    if request.method == 'POST':
        data = json.load(request)
        user_index = data['user_index']
        comment = data['user_text']
        img = data['img']
        img_content = base64.b64decode(img)
        img_result = SimpleUploadedFile('temp.jpg',img_content,getattr(img, "content_type", "application/octet-stream"))

        #request[u'file'] = img_result
        setattr(request, u'file', img_result)
        opponent_photo_index = data['opponent_photo_index']


        user_obj = User.objects.filter(index = user_index)
        if len(user_obj) == 0 :
            return HttpResponse("no user")
        
        user_obj = user_obj[0]

        #photo_obj = Photo(user = user_obj, img = request[u'file'], text = img_text)
        photo_obj = Photo(user = user_obj, img = img_result, text = comment)

        photo_obj.save()
  

        opponent_photo_obj = Photo.objects.filter(index = opponent_photo_index)
        if len(opponent_photo_obj) == 0 :
            return HttpResponse("no photo")

        opponent_photo_obj = opponent_photo_obj[0]

        new_battle = Battle_Log(p1_id = opponent_photo_obj, p2_id = photo_obj)

        new_battle.save()

        return HttpResponse("success")

    return HttpResponse("bad access")


@csrf_exempt
def show_battles(request):
    if request.method == 'POST':
        data = json.load(request)
        user_index = data['user_index']

        #likes = Like_table.objects.filter(user_id = user_obj)
        likes_id_list = []
        likes_list = Like_table.objects.filter(user_id = user_index)
                
        for like in likes_list:
            likes_id_list.append(like.battle_log_id.index)

        
        battles = Battle_Log.objects.exclude(index__in = likes_id_list).order_by('-created_at')
        
        if len(battles) == 0:
          json_obj = {'result': [0]}
          return HttpResponse(json.dumps(json_obj), content_type="application/json")
        user_nickname_list = list()
        for battle in battles:
          user_nickname_list.append([battle.p1_id.user.nickname, battle.p2_id.user.nickname])
        json_encode = make_json_arr(battles)
        json_decode = json.loads(json_encode)
        counter = 0
        for json_obj in json_decode['battles'] :
          json_obj['nickname'] = user_nickname_list[counter]
          counter += 1

        json_encode = json.dumps(json_decode)
        #serialized_obj = [ serializers.serialize('json', [ battle, ]) for battle in battles]
        #json_encode = json.dumps(serialized_obj)
        
        return HttpResponse(json_encode, content_type= "application/json")
    return HttpResponse("bad access")

@csrf_exempt
def show_battles_in_web(request):
    if request.method == 'POST':
        data = json.load(request)
        user_index = data['user_index']
        battle_log_id = data['battle_log_id']
        vote_count = data['count']

        #likes = Like_table.objects.filter(user_id = user_obj)
        likes_id_list = []
        likes_list = Like_table.objects.filter(user_id = user_index)
        for like in likes_list:
            likes_id_list.append(like.battle_log_id.index)
          
        
        battle = Battle_Log.objects.exclude(index__in = likes_id_list).order_by('-created_at')

        json_encode = make_json_arr(battle)
        #serialized_obj = [ serializers.serialize('json', [ battle, ]) for battle in battles]
        #json_encode = json.dumps(serialized_obj)

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
        user_like_list = Like_table.objects.filter(user_id = user_obj).order_by('-created_at')

        if len(user_like_list) == 0 :
            return HttpResponse("no battle you like")

        hit_count = 0
        user_like_battles = list()
        like_photos = list()
        for like in user_like_list:
            user_like_battles.append(like.battle_log_id)
            if (like.battle_log_id.finish is True) and (like.battle_log_id.finished_at is not None):
              winner_photo_index = like.battle_log_id.p1_id.index if like.battle_log_id.p1_vote >= like.battle_log_id.p2_vote else like.battle_log_id.p2_id.index
              if like.photo_id.index == winner_photo_index:
                hit_count += 1
              
            like_photos.append(like.photo_id.index)
        json_encode = make_json_arr(user_like_battles)
        json_decode = json.loads(json_encode)
        counter = 0
        for json_obj in json_decode['battles']:
            json_obj['liked_photo'].append(like_photos[counter])
            counter += 1

        json_decode['liked_photo_count'] = counter + 1
        json_decode['hit_count'] = hit_count
        json_encode = json.dumps(json_decode)
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
            if like.checked == False and like.battle_log_id.finish == True:
                unchecked_list.append(like.battle_log_id)
                like.checked = True
                like.save()
            #elif like.battle_log_id.finish == False:
            #    unchecked_list.append(like.battle_log_id)

        if len(unchecked_list) == 0 :
            return HttpResponse("no battle results")
        
        json_arr = {'vote_info':[]}
        json_obj = {
            'finished_battles_count' : len(unchecked_list),
            'vote_count' : user_obj.vote,
            'win_vote_count' :  user_obj.win_vote
            }
        #json_encode = make_json_arr(unchecked_list)

        json_encode = json.dumps(json_obj)
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

        #photo_obj = photo_obj[0]
        my_battles = Battle_Log.objects.filter((Q(p1_id__in = photo_obj) | Q(p2_id__in = photo_obj))).order_by('-created_at')


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

      

        my_battles = Battle_Log.objects.filter((Q(p1_id__in = photo_obj) | Q(p2_id__in = photo_obj)), finish = True).order_by('-finished_at')

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
def history_info(request):
    if request.method == 'POST':
        data = json.load(request)
        user_index = data['user_index']


        user_obj = User.objects.filter(index = user_index)

        if len(user_obj) == 0:
            return HttpResponse("no user")

        user_obj = user_obj[0]

        photos = Photo.objects.filter(user = user_obj)

        if len(photos) == 0 :
            return HttpResponse("no photos")

        battles = Battle_Log.objects.filter(Q(p1_id__in = photos) | Q(p2_id__in = photos))

        if len(battles) == 0:
            return HttpResponse("no battles")

        total_vote_count = 0

        json_arr = {'battles' : []}
        
        for battle in battles :
            total_vote_count += (battle.p1_vote + battle.p2_vote)
            json_arr['battles'].append(battle.index)
        
        json_obj = {
            'total_vote_count' : total_vote_count,
            'my_vote' : user_obj.my_vote,
            'user_name': user_obj.nickname
            }

        json_arr['history_info'] = json_obj


        json_encode = json.dumps(json_arr)


        return HttpResponse(json_encode, content_type="application/json")
    return HttpResponse("bad access")

        
        
    
  

@csrf_exempt
def vote(request):
    if request.method == "POST":
        data =json.load(request)
        user_index =  data["user_index"]
        liked_photo = data["liked_photo"]
        battle_log_index = data["battle_log"]
        json_arr = {'result' : []}

        user_obj = User.objects.filter(index = user_index)
        if len(user_obj) == 0:
            json_arr['result'].append("0")
            return HttpResponse()
        user_obj = user_obj[0]
        


        battle = Battle_Log.objects.filter(index = battle_log_index)
        if len(battle) == 0:
            json_arr['result'].append("0")
            return HttpResponse("no battle")
        battle = battle[0]

        photo = Photo.objects.filter(index = liked_photo)
        if len(photo) == 0:
            json_arr['result'].append("0")
            return HttpResponse("no photo")
        photo = photo[0]

        

        if Like_table.objects.filter(user_id =user_obj, battle_log_id = battle).count() > 0 :
          json_arr['result'].append("1")
        else :
          like_log = Like_table(user_id = user_obj, battle_log_id = battle, photo_id = photo)
          like_log.save()
          json_arr['result'].append("1")

        return HttpResponse(json.dumps(json_arr), content_type="application/json")
    return HttpResponse("bad access")


@csrf_exempt
def vote_list(request, battle_index):
    json_obj = {'result': []}

    if not battle_index:
      json_obj['result'].append(0)
      return HttpResponse(json.dumps(json_obj), content_type="application/json")
    try:
      battle_obj = Battle_Log.objects.get(index = battle_index)
      like_table_obj = Like_table.objects.filter(battle_log_id = battle_obj, photo_id = battle_obj.p1_id if request.GET.get('vote', '') == 'front' else battle_obj.p2_id )
      json_obj['users'] = []
      for like in like_table_obj : 
        json_obj['users'].append({'user_index' : like.user_id.index, 'user_nickname' : like.user_id.nickname})

      json_obj['result'].append(1)
      
    except Battle_Log.DoesNotExist:
      json_obj['result'].append(0)
    
    return HttpResponse(json.dumps(json_obj), content_type="appliction/json")
