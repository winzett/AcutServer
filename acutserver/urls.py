from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^uploadpage',views.uploadpage, name='uploadpage'),
    url(r'^downloadpage',views.downloadpage, name='downloadpage'),
    url(r'^upload',views.upload, name='upload'),
    url(r'^download',views.download, name='download'),
]

