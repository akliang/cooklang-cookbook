from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  render, redirect
from .forms import LoginForm, RegisterForm, ModifyRecipe
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .cooklang_processor import process as clprocess
from django.contrib.auth import authenticate, login


def index(request):
  if request.user.is_authenticated:
    return HttpResponse("Hello, world. You're at the polls index.")
  else:
    return HttpResponseRedirect('/login')

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
      return HttpResponseRedirect(request.POST.get('next'))
    else:
      return HttpResponseRedirect('/')
  else:
    login_form = LoginForm()
    return render(request=request, template_name="web/login.html", context={"form":login_form})

def logout(request):
  auth_logout(request)
  return HttpResponseRedirect('/')

def register(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)

    if form.is_valid():
      if form.cleaned_data['password'] != form.cleaned_data['password2']:
        return HttpResponse("Password doesn't match.")
      else:
        user = form.save()
        auth_login(request, user)
        return redirect("web:index")
    else:
      return HttpResponse("Registration error.")
  else:
    form = RegisterForm()
    return render(request=request, template_name="web/register.html", context={"form":form})

@login_required
def recipe(request):
  if request.method == 'POST':
    form = ModifyRecipe(request.POST)
    if form.is_valid():
      filename = form.cleaned_data['title'].replace(" ","-").lower()
      with open(f"./data/recipes/{request.user.username}/{filename}.cook", "w") as file:
        file.write(f">> title: {form.cleaned_data['title']}\n")
        file.write(f">> tags: {form.cleaned_data['tags']}\n")
        file.write(form.cleaned_data['recipe'])
      
      return HttpResponseRedirect('/')
  else:
    form = ModifyRecipe()

  return render(request, 'web/recipe.html', {'form': form})

def view(request, username, title):
  title = title.lower()
  data = clprocess(f"./data/recipes/{username}/{title}.cook")

  if request.user.is_authenticated and request.user.username == username:
    edit = True
  else:
    edit = False

  return render(request=request, template_name="web/view.html", context={'data': data, 'edit': edit})
