from django import forms

class upload_image_form(forms.Form):
  image = forms.ImageField()
