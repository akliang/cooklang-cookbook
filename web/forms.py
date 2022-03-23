from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Chef


# Create your forms here.

class LoginForm(forms.Form):
  username = forms.CharField(
    max_length=255,
    widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': 'autofocus'}),
    required=True,
  )

  password = forms.CharField(
    max_length=255,
    widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    required=True
  )

class RegisterForm(forms.Form):
  username = forms.CharField(
    max_length=255,
    widget=forms.TextInput(attrs={'placeholder': 'Username'}),
    required=True,
  )

  email = forms.EmailField(
    max_length=255,
    widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
    required=True,
  )

  password = forms.CharField(
    max_length=255,
    widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    required=True
  )

  password2 = forms.CharField(
    max_length=255,
    widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
    required=True
  )

  def save(self):
    user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
    Chef.objects.create(user=user, email=self.cleaned_data['email'])
    return user

class ModifyRecipe(forms.Form):
  title = forms.CharField(
    max_length=255,
    widget=forms.TextInput(attrs={'placeholder': 'Recipe Title'}),
    required=True
  )
  tags = forms.CharField(
    max_length=255,
    widget=forms.TextInput(attrs={'placeholder': 'Tags'})
  )
  recipe = forms.CharField(
    widget=forms.Textarea(attrs={'placeholder': 'Recipe goes here'})
  )

