from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from acutserver.form.forms import upload_image_form
from django.db import connection
from acutserver.core.models import User,Photo

def signin_test(request):
  return render(request,"./jsontest.html")

def json_decoding_page(request):
  return render(request,"./json_decode.html")

@csrf_exempt
def json_decode(request):
  if 'shiny' in request.POST:
    decode_rt=request.POST['name']+", "+request.POST['hind']
  else:
    decode_rt="no json object or no check on the check box"
  return HttpResponse("<h1> %s </h1>" %decode_rt)

def uploadpage(request) :
  return render(request, './upload.html')

def downloadpage(request) :
  return render(request, './download.html')
@csrf_exempt
def upload(request) :
  if request.method == 'POST':
    form = upload_image_form(request.POST, request.FILES)

    user_obj = User.objects.filter(index = request.POST.get('username',False))

    #if form.is_valid():
    image_file = Photo(user = user_obj[0] ,img = request.FILES['image'])
    image_file.save()

    return HttpResponse("%s" %image_file.img)
  return HttpResponse("<h1>upload fail</h1>")

@csrf_exempt
def download(request) :
  cursor = connection.cursor()
  query_string = "select image from acutserver_upload_file where user_index = \"%s\"" %request.POST.get('username',False)
  cursor.execute(query_string)
  result = cursor.fetchall()
  image_url = "https://s3.ap-northeast-2.amazonaws.com/acut-fullsize-image/"

  if cursor.rowcount != 0 :
    image_list = []
    result_str = ""

    for row in result :
      image_list.append(image_url+str(row[0]).encode('euc-kr'))
      result_str += "<img src=\""+image_url+str(row[0])+"\">"

    return HttpResponse("%s" %result_str)

  return HttpResponse("<h1>download fail</h1>")
