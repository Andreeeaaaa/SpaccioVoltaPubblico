from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields

from .models import Profile
# File to create forms that inherit from django's user creation forms
# They need to be added to the views file to be displayed

# ATTENTION: You don't need to specify a new forms field in these sezioni if it already exists in the model
# just include it in the fields list in the meta class

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required = True)
    nome = forms.CharField(max_length=40)
    cognome = forms.CharField(max_length=40)
    user_class = forms.CharField(max_length=2, label='Classe', required=False, help_text='Se non sei di nessuna classe, lascia il campo vuoto.')

    class Meta:
        # In this class you need to specify the model you want this form to interact with
        # it gives us a nested namespace for config. 
        model = User  # Model that will be affected (changed, saved to)
        fields = ['username', 'email', 'password1', 'password2']  # Fields that we want in the forms in order


# The model form allows us to create a form that will work with a specific db model
# in this case, it updates our user module (but not the password)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        # In this class you need to specify the model you want this form to interact with
        # it gives us a nested namespace for config. 
        model = User  # Model that will be affected (changed, saved to)
        fields = ['username', 'email']  # Fields that we want in the forms in order

# Form that updates our profile module (the image)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nome', 'cognome', 'classe']

