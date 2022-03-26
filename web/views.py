import os
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, RegisterForm, ModifyRecipe
from .cooklang_processor import process as clprocess
from web.helpers import write_formdata_to_cookfile


def index(request):
  if request.user.is_authenticated:
    return HttpResponse("Hello, world. You're at the polls index.")
  else:
    return redirect('web:login')

def login(request):
  if request.method == "POST":
    form = LoginForm(request.POST)
    if form.is_valid():
      user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
      if user is not None:
        auth_login(request, user)

  # at this point, you are either logged in or not
  if request.user.is_authenticated:
    if request.POST.get('next'):
      return redirect(request.POST.get('next'))
    else:
      return redirect('web:index')
  else:
    login_form = LoginForm()
    return render(request=request, template_name="web/login.html", context={"form":login_form})

def logout(request):
  auth_logout(request)
  return redirect('web:index')

def register(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)

    if form.is_valid():
      if form.cleaned_data['password'] != form.cleaned_data['password2']:
        return HttpResponse("Password doesn't match.")
      else:
        user = form.save()
        auth_login(request, user)
        # create the user folder for recipes
        os.mkdir(os.path.join('data','recipes',form.cleaned_data['username']))
        return redirect("web:index")
    else:
      return HttpResponse("Registration error.")
  else:
    form = RegisterForm()
    return render(request=request, template_name="web/register.html", context={"form":form})

@login_required
def recipe(request):
  if request.method == 'POST':
    # if the edit flag is found, then enter edit-mode
    if request.POST.get("edit"):
      # rearrange the request.POST data so it fits into the form
      form_data = {}
      meta = request.POST.get('meta')
      # meta is a literal string with single quotes, but we need to conver it back into a dict
      meta = json.loads(meta.replace("'", '"'))
      for key,value in meta.items():
        form_data[key] = value
      form_data['recipe'] = request.POST.get('recipe')
      form = ModifyRecipe(form_data)
      return render(request, 'web/recipe.html', {'form': form})
    else:
      # otherwise, assume we are inserting a new recipe
      form = ModifyRecipe(request.POST)
      # write the form data to cook file
      if form.is_valid():
        filename = write_formdata_to_cookfile(request, form.cleaned_data)
        return redirect('web:view', username=request.user.username, filename=filename)
      else:
        # send them back to the recipe form with prepopulated fields
        return render(request, 'web/recipe.html', {'form': form})
  else:
    # render the blank form
    form = ModifyRecipe()
    return render(request, 'web/recipe.html', {'form': form})

def view(request, username, filename):
  filename = filename.lower()
  data = clprocess(f"./data/recipes/{username}/{filename}.cook")

  if request.user.is_authenticated and request.user.username == username:
    edit = True
  else:
    edit = False

  return render(request=request, template_name="web/view.html", context={'data': data, 'edit': edit})
