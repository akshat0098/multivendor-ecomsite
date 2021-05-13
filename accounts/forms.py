from .models import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms
#Creating the form

User = get_user_model()

choices = (('Electrical','Electrical'),
    ('Carpenter','Carpenter'),
    ('Plumbing','Plumbing'),
   ('Hardware','Hardware'),
)



class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']



choices = (('Electrical','Electrical'),
    ('Carpenter','Carpenter'),
    ('Plumbing','Plumbing'),
   ('Hardware','Hardware'),
)
  

class VendorRegistrationForm(UserCreationForm):

    Name = forms.CharField(max_length=100)
    phone_no = forms.CharField(max_length=10)
    TRADE_NAME = forms.CharField(max_length=150)
    office_address = forms.CharField(max_length=200)
    NATURE_OF_SUPPLY = forms.ChoiceField(choices=choices)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
