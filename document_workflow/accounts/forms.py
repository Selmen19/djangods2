from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # You can add more custom fields here if necessary
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # Adjust fields as needed
