from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  render, redirect
from .forms import NewUserForm, ModifyRecipe
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def register(request):
  if request.method == "POST":
    form = NewUserForm(request.POST)

    if form.is_valid():
      user = form.save()
      login(request, user)
      messages.success(request, "Registration successful." )
      return redirect("web:index")
    messages.error(request, "Unsuccessful registration. Invalid information.")
  
  form = NewUserForm()
  return render (request=request, template_name="web/register.html", context={"register_form":form})

@login_required
def recipe(request):
  if request.method == 'POST':
    form = ModifyRecipe(request.POST)
    if form.is_valid():
      with open(f"./data/{request.user.username}/{form.cleaned_data['title']}.txt", "w") as file:
        file.write(f">> title: {form.cleaned_data['title']}\n")
        file.write(f">> tags: {form.cleaned_data['tags']}\n")
        file.write(form.cleaned_data['recipe'])
      
      return HttpResponseRedirect('/')
  else:
    form = ModifyRecipe()

  return render(request, 'web/recipe.html', {'form': form})