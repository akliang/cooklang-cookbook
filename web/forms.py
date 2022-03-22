from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class ModifyRecipe(forms.Form):
  title = forms.CharField(
    label='Recipe title',
    max_length=255,
    widget=forms.TextInput(attrs={'placeholder': 'Recipe Title'}),
    required=True)
  tags = forms.CharField(
    label='Tags',
    max_length=255,
      widget=forms.TextInput(attrs={'placeholder': 'Tags'}))
  recipe = forms.CharField(
    widget=forms.Textarea(attrs={'placeholder': 'Recipe goes here'}))

