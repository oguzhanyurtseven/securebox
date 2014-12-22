__author__ = 'oguzhan'
from django import forms
from models import *


class new_user_form(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    email = forms.CharField(max_length=150)


class send_mail_form(forms.ModelForm):
    class Meta:
        model = message
        widgets = {'user': forms.HiddenInput(),
                   'message': forms.Textarea}


class decrypt_page_input_form(forms.Form):
    salt = forms.CharField(max_length=50)
    message = forms.CharField(max_length=1000)


