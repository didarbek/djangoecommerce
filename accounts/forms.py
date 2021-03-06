from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Profile

class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['email'].widget.attrs['required'] = 'required'
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",
        ]


class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender',]