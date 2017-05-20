from django import forms
from acutserver.models import User
class upload_image_form(forms.Form):
  image = forms.ImageField()


class user_form(forms.Form):
  class Meta :
    model = User
    field = ['user_index', 'user_id','user_pw','user_name','user_email']

