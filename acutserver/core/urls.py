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
    #url(r'^uploadpage',test.uploadpage, name='uploadpage'),
    #url(r'^downloadpage',test.downloadpage, name='downloadpage'),
    #url(r'^json_decode',test.json_decode, name='json_decode'),
    #url(r'^jsontest_page', test.jsontest, name='jsontest'),
    #url(r'^json_decoding_page',test.json_decoding_page, name='json_decoding_page'),
    #url(r'^upload',test.upload, name='upload'),
    #url(r'^download',test.download, name='download'),

    #url(r'^sign_up', membership_management.sign_up, name='sign_up'),
    #url(r'^sign_in', membership_management.sign_in, name='sign_in'),
    
    #url(r'^post_photo', post_and_comment.user_posts, name='user_post'),
    #url(r'^test_page', test_page.uploadpage, name="upload"),
    url(r'^sign_in', membership_management.sign_in, name='sign_in'),
    url(r'^upload_img', test_page.upload, name='upload'),
    url(r'^upload_page', test_page.uploadpage, name='upload_page'),
    url(r'^show_lounge', photo_management.show_lounge, name='lounge'),
    url(r'^show_battles', battle_management.show_battles, name='show_battles'),
    url(r'^create_photo', photo_management.create, name='create'),
    url(r'^show_battle_results', battle_management.show_battle_results, name='show_battle_results'),
     url(r'^show_battles', battle_management.show_battles,'show_battles'),

    ]
#router = routers.DefaultRouter()
#router.register(r'users',UserViewSet)
#router.register(r'photos', PhotoViewSet)

#urlpatterns = [
      #url(r'^docs/', include('rest_framework_swagger.urls')),
#    ]
#urlpatterns += router.urls
