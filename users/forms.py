from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email','phone_number', 'role']
        
        
        
class CustomAuthenticationForm(AuthenticationForm):
    
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password']