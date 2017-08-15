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
def sign_up(request) :
    if request.method =='POST':
        data = json.load(request)
        data['pw'] = pbkdf2_sha256.hash(data['pw'])
        img = data['img']

        img_content = base64.b64decode(img)
        img_result = SimpleUploadedFile('temp.jpg', img_content ,getattr(img,"content_type","application/octet-stream"))

        request.FILES[u'file'] = img_result

        p_img = ""

        user_obj = User(user_name = data['user_name'],
                        user_id = data['user_id'],
                        pw = data['pw'],
                        nickname = data['nickname'],
                        profile_thumb = request.FILES[u'file'],
                        email = data['email']
                        )

        form = user_form(data)
        if form.is_valid :
            form.save()
            return HttpResponse("save")
        else :
            return HttpResponse("save fail")

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
