from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class LoginForm(forms.Form):
  username = forms.CharField(
    max_length=255,
    widget=forms.TextInput(attrs={'placeholder': 'Username'}),
    required=True,
  )

  password = forms.CharField(
    max_length=255,
    widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    required=True
  )

  class Meta:
    model = User
    fields = ("username", "password")

	# def save(self, commit=True):
	# 	user = super(NewUserForm, self).save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 	return user

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

