from django.conf.urls import url

from .views import test
from .views import membership_management
from .views import post_and_comment
urlpatterns =[
    url(r'^uploadpage',test.uploadpage, name='uploadpage'),
    url(r'^downloadpage',test.downloadpage, name='downloadpage'),
    url(r'^json_decode',test.json_decode, name='json_decode'),
    url(r'^jsontest_page', test.jsontest, name='jsontest'),
    url(r'^json_decoding_page',test.json_decoding_page, name='json_decoding_page'),
    url(r'^upload',test.upload, name='upload'),
    url(r'^download',test.download, name='download'),

    url(r'^sign_up', membership_management.sign_up, name='sign_up'),
    url(r'^sign_in', membership_management.sign_in, name='sign_in'),
    
    url(r'^post_photo', post_and_comment.user_posts, name='user_post'),

    ]

