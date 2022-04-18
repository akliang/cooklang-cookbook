from django import forms
from django.contrib.auth.models import User
from api.models import Chef

# class RegisterForm(forms.Form):
#   username = forms.CharField(
#     max_length=255,
#     widget=forms.TextInput(attrs={'placeholder': 'Username'}),
#     required=True,
#   )

#   email = forms.EmailField(
#     max_length=255,
#     widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
#     required=True,
#   )

#   password = forms.CharField(
#     max_length=255,
#     widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
#     required=True
#   )

#   password2 = forms.CharField(
#     max_length=255,
#     widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
#     required=True
#   )

#   def save(self):
    # user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
    # Chef.objects.create(user=user, email=self.cleaned_data['email'])
    # return user

class RecipeForm(forms.Form):
  title = forms.CharField(
    max_length=255
  )
  tags = forms.CharField(
    max_length=255,
    required=False
  )
  recipe = forms.CharField()

