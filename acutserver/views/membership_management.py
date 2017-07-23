from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from acutserver.form.forms import user_form
from acutserver.core.models import User
from passlib.apps import custom_app_context as pwd_context


import json

@csrf_exempt
def sign_up(request) :
    if request.method =='POST':
        data = json.load(request)
        data['user_pw'] = pwd_context.hash(data['user_pw'])

        if form.is_valid :
            form.save()
            return HttpResponse("save")
        else :
            return HttpResponse("save fail")

    return HttpResponse("bad access")


@csrf_exempt
def sign_in(request):
    if request.method =='POST':

        json_obj = json.load(request)
        data = json_obj[0]
        #data = request.POST

        u_id = data['user_id']

        res = User.objects.filter(user_id = u_id).values("index","user_name","profile_thumb","email")

        if res.exists():
            sign_in_user = res[0]
            hashed_pw = sign_in_user.user_pw

            if not pwd_context.verify(data['user_pw'], hashed_pw):
                return HttpResponse("wrong pw")

        else :
            return HttpResponse("there is no matched id and pw")

        return HttpResponse(json.dumps(sign_in_user), content_type="application/json")

    return HttpResponse("bad access")
