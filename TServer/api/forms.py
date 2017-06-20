from django import forms

from .models import User


class UserJoinForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('id', 'password', 'email', )

