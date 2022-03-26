import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from web.forms import LoginForm, RegisterForm


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

