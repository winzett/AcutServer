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
from acutserver.views import post_management
from acutserver.core.mailer import *

urlpatterns =[
    #url(r'^api_auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    url(r'^testsign_in', test_page.signin_test, name='sign_in_test'),
    url(r'^sign_in', membership_management.sign_in, name='sign_in'),
    url(r'^email_varification', membership_management.varifying_email, name='varification'),
    url(r'^upload_img', test_page.upload, name='upload'),
    url(r'^sign_up', membership_management.sign_up, name='sign_up'),
    url(r'^change_user_info', membership_management.change_user_info, name='change_user_info'),
    url(r'^upload_page', test_page.uploadpage, name='upload_page'),
    url(r'^show_lounge', photo_management.show_lounge, name='lounge'),
    url(r'^create_photo', photo_management.create, name='create'),
    url(r'^show_my_lounge', photo_management.show_my_lounge, name='my_lounge'),
    url(r'^change_photo_info', photo_management.change_photo_info, name='change_photo_info'),
    url(r'^show_battles', battle_management.show_battles, name='show_battles'),
    url(r'^show_liked_battles', battle_management.show_liked_battles, name='show_liked_battles'),
    
    url(r'^battle/(?P<battle_index>[0-9]+)/vote_list', battle_management.vote_list, name='battle_vote_list'),
    url(r'^notice/(?P<post_index>[0-9]+)', post_management.show, name='notice_show'),
    url(r'^show_liked_battle_results', battle_management.show_liked_battle_results, name='show_liked_battle_results'),
    url(r'^show_my_battles', battle_management.show_my_battles, name='show_my_battles'),
    url(r'^show_my_battle_results', battle_management.show_my_battle_results, name='show_my_battle_results'),
    url(r'^have_battle', battle_management.have_battle, name='have_battle'),
    url(r'^vote', battle_management.vote, name='vote'),
     url(r'^history_info', battle_management.history_info, name='history_info'),
    url(r'^send_mail', test_mail, name='test_mail' ),
    url(r'^notice/create', post_management.create, name='notice_create'),
    url(r'^notice/delete', post_management.delete, name='notice_delete'),
    url(r'^notice/edit', post_management.edit, name='notice_edit'),
    url(r'^notice', post_management.index, name='notice'),
    #url(r'^(?P<post_index>[0-9]+)/notice/$', post_management.show, name='notice_show'),
    #url(r'', include('gcm.urls'), name='gcm'),
    #url(r'^send_test_mail', test_test_mail(), name='test_test_mail' ),
    #url(r'^send_mailing', mailing(), name='mailing' ),



    ]
#router = routers.DefaultRouter()
#router.register(r'users',UserViewSet)
#router.register(r'photos', PhotoViewSet)

#urlpatterns = [
      #url(r'^docs/', include('rest_framework_swagger.urls')),
#    ]
#urlpatterns += router.urls
