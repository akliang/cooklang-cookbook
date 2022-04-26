from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from api.models import Recipe

def validate_email(value):
    if User.objects.filter(email = value).exists():
      # note: the params struct is to keep with best-practice for ValidationError per Django documentation
      raise ValidationError((f"Email {value} is taken."), params = {'value': value})  

class ChefCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators = [validate_email])

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(ChefCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# class RecipeForm(forms.Form):
#   title = forms.CharField(max_length=255)
#   tags = forms.CharField(max_length=255, required=False)
#   recipe = forms.CharField()

class RecipeForm(forms.ModelForm):
  class Meta:
    model = Recipe
    fields = ['title', 'tags', 'recipe', 'image']

  def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['tags'].required = False
        self.fields['image'].required = False