from django.conf.urls import url, include
#from rest_framework import routers
#from .views import UserViewSet, PhotoViewSet
#from core.views import 
#from acutserver.views import test
#from acutserver.views import membership_management
#from acutserver.views import post_and_comment
from acutserver.views import membership_management
from acutserver.views import test_page
from acutserver.views import photo_management
from acutserver.views import battle_management

urlpatterns =[
    #url(r'^api_auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    url(r'^sign_in', membership_management.sign_in, name='sign_in'),
    url(r'^upload_img', test_page.upload, name='upload'),
    url(r'^upload_page', test_page.uploadpage, name='upload_page'),
    url(r'^show_lounge', photo_management.show_lounge, name='lounge'),
    url(r'^show_battles', battle_management.show_battles, name='show_battles'),
    url(r'^create_photo', photo_management.create, name='create'),
    url(r'^show_liked_battles', battle_management.show_liked_battles, name='show_liked_battles'),
    url(r'^show_liked_battle_results', battle_management.show_liked_battle_results, name='show_liked_battle_results'),
    url(r'^show_my_battles', battle_management.show_my_battles, name='show_my_battles'),
    url(r'^show_my_battle_results', battle_management.show_my_battle_results, name='show_my_battle_results'),

     url(r'^show_battles', battle_management.show_battles,'show_battles'),

    ]
#router = routers.DefaultRouter()
#router.register(r'users',UserViewSet)
#router.register(r'photos', PhotoViewSet)

#urlpatterns = [
      #url(r'^docs/', include('rest_framework_swagger.urls')),
#    ]
#urlpatterns += router.urls
