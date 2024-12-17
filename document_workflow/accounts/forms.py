# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Document

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # Adjust fields as needed


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

    def __str__(self):
        return self.instance.title  # Using self.instance to reference the model instance
