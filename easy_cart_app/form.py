from django.contrib.auth.forms import UserCreationForm  # forms for authentication for users
from .models import User
from django import forms

# Overwrite the default User forms as a custom form
class CustomUserForm(UserCreationForm):
    # Custom styles for the forms
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border-2 border-gray-400 outline-violet-600 rounded-sm py-1 px-2', 'placeholder': 'Enter the username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'w-full border-2 border-gray-400 outline-violet-600 rounded-sm py-1 px-2', 'placeholder': 'Enter the Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full border-2 border-gray-400 outline-violet-600 rounded-sm py-1 px-2', 'placeholder': 'Enter the Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full border-2 border-gray-400 outline-violet-600 rounded-sm py-1 px-2', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']