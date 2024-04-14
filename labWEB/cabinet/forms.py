from django import forms
from .models import UserTheme, UserToken


class UserThemeForm(forms.ModelForm):
    class Meta:
        model = UserTheme
        fields = ['theme']

class UserTokenForm(forms.ModelForm):
    class Meta:
        model = UserToken
        fields = ['token']
