from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^uploadpage',views.uploadpage, name='uploadpage'),
    url(r'^downloadpage',views.downloadpage, name='downloadpage'),
    url(r'^upload',views.upload, name='upload'),
    url(r'^download',views.download, name='download'),
    url(r'^json_decoding_page',views.json_decoding_page, name='json_decoding_page'),
    url(r'^json_decode',views.json_decode, name='json_decode'),
    #url(r'^delete_photopage',views.delete_photopage, name='delete_photopage'),
    #url(r'^delete_photo',views.delete_photo, name='delete_photo'),
    url(r'^sign_up', views.sign_up, name='sign_up'),
    url(r'^sign_in', views.sign_in, name='sign_in'),
    url(r'^jsontest_page', views.jsontest, name='jsontest'),    
    ]

