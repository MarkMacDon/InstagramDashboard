from .models import Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, EmailInput

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    #This Meta class gives nested namespace for config and keeps it in one place
    #Here it will be saved to the User model
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['handle', 'image']

class AuthForm(AuthenticationForm):

    class Meta:
        widgets = {
            'username':forms.EmailInput(attrs={'class':'form-control form-control-sm'}),
            'password':forms.PasswordInput(attrs={'class':'form-control form-control-sm'}),
        }