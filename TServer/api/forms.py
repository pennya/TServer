from django import forms

from .models import User
from .models import Star


class UserJoinForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('id', 'password', 'email', )


class StarForm(forms.ModelForm):
    class Meta:
        model = Star
        fields = ('restaurant', 'user', 'rating',)