import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from api.forms import ModifyRecipe
from api.cooklang_processor import process as clprocess
from api.helpers import write_formdata_to_cookfile

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
