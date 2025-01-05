from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from main.models import WiseUser


class UserLoginForm(AuthenticationForm):
  username = forms.CharField() 
  password = forms.CharField()

  class Meta:
    model = WiseUser


class UserRegistrationForm(UserCreationForm):
  class Meta:
    model = WiseUser
    fields = (
      "username",
      "password1",
      "password2",
      "email",
    )
  
  username = forms.CharField()
  password1 = forms.CharField()
  password2 = forms.CharField()
  email = forms.EmailField()


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)