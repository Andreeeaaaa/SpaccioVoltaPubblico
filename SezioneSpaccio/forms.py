from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        # In this class you need to specify the model you want this form to interact with
        # it gives us a nested namespace for config. 
        model = User  # Model that will be affected (changed, saved to)
        fields = ['email']  # Fields that we want in the forms in order