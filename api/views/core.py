

from api.forms import RecipeForm
from api.helpers.cooklang import cooklang_processor as clprocess
from api.views.authentication import lookup_user_by_api
from rest_framework.views import APIView
import os
import re
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from api.models import Recipe
from api.serializers import RecipeSerializer

class RecipeView(APIView):
  def get(self, request, *args, **kw):
    recipe = Recipe.objects.get(slug=kw['slug'], chef__username=kw['username'])
    # TODO: if no recipe, return error

    print(recipe.recipe)
    proc_recipe = clprocess(recipe.recipe)
    
    user = lookup_user_by_api(request)
    if user == recipe.chef:
      edit = kw['slug']
    else:
      edit = False
    # TODO: convert to serializer
    return Response({'title': recipe.title, 'ingredients': proc_recipe['ingredients'], 'recipe': proc_recipe['recipe'], 'edit': edit})

class GetReceipeWithToken(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    return Response(clprocess(f"./data/recipes/{user.username}/{kw['recipe']}.cook"))

class MyRecipes(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if user:
      recipes = Recipe.objects.filter(chef=user)
      serialized = RecipeSerializer(recipes, many=True)
      return JsonResponse(serialized.data, safe=False)
    else:
      return Response("Error")

class AddRecipe(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    form = RecipeForm(request.POST)
    # write the form data to cook file
    if form.is_valid():
      # build the slug, first remove all non-alphanumeric characters
      slug = re.sub('[^a-zA-Z0-9 ]', '', form.cleaned_data['title'])
      slug = re.sub('\s', '-', slug)
      slug = slug.lower()

      obj = form.save(commit=False)
      obj.chef = user
      obj.slug = slug
      obj.image = ""
      obj.save()

      return Response({
        'username': user.username,
        'slug': slug
      }, status=status.HTTP_201_CREATED)
    else:
      return Response(form.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteRecipe(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    recipe = Recipe.objects.get(slug=kw['slug'], chef=user)

    if recipe:
      recipe.delete()
      return Response(True)
    else:
      return Response(None)