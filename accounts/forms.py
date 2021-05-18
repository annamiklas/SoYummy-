from accounts.models import UserProfile
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *argv, **kwargs):
        super(RegistrationForm, self).__init__(*argv, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username...'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email..'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password...'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter password...'

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'card__input'



class CookForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['cook_img','description']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

