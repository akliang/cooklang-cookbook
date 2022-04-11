import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from api.forms import ModifyRecipe
from api.helpers import cooklang_processor as clprocess
from api.helpers import write_formdata_to_cookfile
from rest_framework.views import APIView
import os
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator

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
      return render(request, 'api/recipe.html', {'form': form})
    else:
      # otherwise, assume we are inserting a new recipe
      form = ModifyRecipe(request.POST)
      # write the form data to cook file
      if form.is_valid():
        filename = write_formdata_to_cookfile(request, form.cleaned_data)
        return redirect('api:view', username=request.user.username, filename=filename)
      else:
        # send them back to the recipe form with prepopulated fields
        return render(request, 'api/recipe.html', {'form': form})
  else:
    # render the blank form
    form = ModifyRecipe()
    return render(request, 'api/recipe.html', {'form': form})

def view(request, username, filename):
  filename = filename.lower()
  data = clprocess(f"./data/recipes/{username}/{filename}.cook")

  if request.user.is_authenticated and request.user.username == username:
    edit = True
  else:
    edit = False

  return render(request=request, template_name="api/view.html", context={'data': data, 'edit': edit})

class MyRecipesView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kw):
    queryset = []
    user_path = f"./data/recipes/{kw['user']}/"
    for filename in os.listdir(user_path):
      queryset.append(clprocess(os.path.join(user_path, filename)))
    return Response(queryset)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(csrf_exempt, name='get')
@method_decorator(ensure_csrf_cookie, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='get')
class RecipeView(APIView):
  authentication_classes = [SessionAuthentication]
  permission_classes = [IsAuthenticated]
  
  @csrf_exempt
  @ensure_csrf_cookie
  def get(self, request, *args, **kw):
    import pprint
    pprint.pprint(request.META)
    return Response(clprocess(f"./data/recipes/{kw['user']}/{kw['recipe']}.cook"))

def recipe_view(request, user, recipe):
  import pprint
  pprint.pprint(request.META)
  pprint.pprint(request.session.session_key)