from django.shortcuts import render
from django.http import HttpResponse
from .models import upload_file
from django.core.urlresolvers import reverse
from .image_form import upload_image_form
from django.views.decorators.csrf import csrf_exempt
#from boto.s3.connection import S3Connection
#from boto.s3.key import key


# Create your views here.

def uploadpage(request) :
  return render(request, './upload.html')

@csrf_exempt
def upload(request) :
  if request.method == 'POST':
    form = upload_image_form(request.POST, request.FILES)
    if form.is_valid():
      image_file = upload_file(user = request.POST.get('username',False), image = request.FILES['image'])
      image_file.save()
      #form.save()
      return HttpResponse("<h1>upload success</h1>")

  return HttpResponse("<h1>upload fail</h1>")


def download(request) :
  return HttpResponse("<h1>this is download page</h1>")
