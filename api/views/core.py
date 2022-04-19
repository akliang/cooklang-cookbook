import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from api.forms import RecipeForm
from api.helpers.cooklang import cooklang_processor as clprocess
from api.helpers.cooklang import write_formdata_to_cookfile
from api.views.authentication import lookup_user_by_api
from rest_framework.views import APIView
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.authentication import get_authorization_header
# from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
# from django.utils.decorators import method_decorator

# @login_required
# def recipe(request):
#   if request.method == 'POST':
#     # if the edit flag is found, then enter edit-mode
#     if request.POST.get("edit"):
#       # rearrange the request.POST data so it fits into the form
#       form_data = {}
#       meta = request.POST.get('meta')
#       # meta is a literal string with single quotes, but we need to conver it back into a dict
#       meta = json.loads(meta.replace("'", '"'))
#       for key,value in meta.items():
#         form_data[key] = value
#       form_data['recipe'] = request.POST.get('recipe')
#       form = ModifyRecipe(form_data)
#       return render(request, 'api/recipe.html', {'form': form})
#     else:
#       # otherwise, assume we are inserting a new recipe
#       form = ModifyRecipe(request.POST)
#       # write the form data to cook file
#       if form.is_valid():
#         filename = write_formdata_to_cookfile(request, form.cleaned_data)
#         return redirect('api:view', username=request.user.username, filename=filename)
#       else:
#         # send them back to the recipe form with prepopulated fields
#         return render(request, 'api/recipe.html', {'form': form})
#   else:
#     # render the blank form
#     form = ModifyRecipe()
#     return render(request, 'api/recipe.html', {'form': form})

# def view(request, username, filename):
#   filename = filename.lower()
#   data = clprocess(f"./data/recipes/{username}/{filename}.cook")

#   if request.user.is_authenticated and request.user.username == username:
#     edit = True
#   else:
#     edit = False

#   return render(request=request, template_name="api/view.html", context={'data': data, 'edit': edit})


class GetReceipeWithToken(APIView):
  def get(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    return Response(clprocess(f"./data/recipes/{user.username}/{kw['recipe']}.cook"))

class RecipeView(APIView):
  def get(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if user and user.username == kw['user']:
      edit = kw['recipe']
    else:
      edit = False
    return Response({'data': clprocess(f"./data/recipes/{kw['user']}/{kw['recipe']}.cook"), 'edit': edit})

class MyRecipes(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    recipes = []
    userpath = f"./data/recipes/{user.username}/"
    for filename in os.listdir(userpath):
      cldata = clprocess(os.path.join(userpath, filename))
      recipes.append({
        'title': cldata['meta']['title'],
        'url': f'{user.username}/{filename.replace(".cook","")}'
      })
    return Response(recipes)

class AddRecipe(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    form = RecipeForm(request.POST)
    print(form.errors)
    # write the form data to cook file
    if form.is_valid():
      filename = write_formdata_to_cookfile(user, form.cleaned_data)
      return Response({
        'username': user.username,
        'filename': filename
      }, status=status.HTTP_201_CREATED)
    else:
      return Response(form.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteRecipe(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)

    if user:
      path_to_file = f"./data/recipes/{user.username}/{kw['recipe']}.cook"
      if os.path.exists(path_to_file):
        os.remove(path_to_file)
        return Response(True)
      else:
        # TODO make this return something meaningful for logging
        return Response(None)
    else:
      return Response(None)