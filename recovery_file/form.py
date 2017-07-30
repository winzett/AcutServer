from django import forms
from acutserver.core.models import User

class upload_image_form(forms.Form):
    image = forms.ImageField()

class user_form(forms.Form):
    class Meta:
        model = User
        field = {'user_name','user_id','pw','nickname','profile_thumb','email',}
