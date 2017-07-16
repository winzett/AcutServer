from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from acutserver.form.forms import user_form
from acutserver.core.models import User

import json

@csrf_exempt
def sign_up(request) :
  if request.method =='POST':
    data = json.load(request)
    """u_id = data['user_id']  
    u_pw = data['user_pw']
    u_name = data['user_name']
    u_email = data['user_email']
    sign_up_obj = User(user_id = u_id, user_pw = u_pw, user_name = u_name,user_email = u_email, user_type = "normal",ticket = 0)
    """
    form = user_form(data)
    """try :
      sign_up_obj.save()
    except Error as e :
      return HttpResponse("%s" %e.message)
    """

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
    u_pw = data['user_pw']
    
    res = User.objects.filter(user_id = u_id, pw = u_pw).values("index","user_name","profile_thumb","email")
    
    if res.exists():
      sign_in_user = res[0]
    else :
      return HttpResponse("there is no matched id and pw")
    
    return HttpResponse(json.dumps(sign_in_user), content_type="application/json")

  return HttpResponse("bad access")


