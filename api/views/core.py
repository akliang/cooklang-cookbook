

from api.forms import RecipeForm
from api.helpers.cooklang import cooklang_processor as clprocess
from api.views.authentication import lookup_user_by_api
from rest_framework.views import APIView
import os
import re
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from api.models import Recipe, Bookmark
from api.serializers import RecipeSerializer

class RecipeView(APIView):
  authentication_classes = ()
  permission_classes = (AllowAny,)

  def get(self, request, *args, **kw):
    recipe = Recipe.objects.get(slug=kw['slug'], chef__username=kw['username'])
    # TODO: if no recipe, return error

    proc_recipe = clprocess(recipe.recipe)
    user = lookup_user_by_api(request)

    if user == recipe.chef:
      edit = True
    else:
      edit = False

    try:
      bookmark = Bookmark.objects.get(chef=user, recipe=recipe)
      bookmarked = True
    except Bookmark.DoesNotExist:
      bookmarked = False

    # TODO: convert to serializer
    return Response({'title': recipe.title, 'ingredients': proc_recipe['ingredients'], 'recipe': proc_recipe['recipe'], 'edit': edit, 'bookmarked': bookmarked})

class GetRecipeWithToken(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    recipe = Recipe.objects.get(slug=kw['slug'], chef=user)
    if recipe:
      return JsonResponse(RecipeSerializer(recipe).data)
    else:
      return Response("Error")

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

class MyBookmarks(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if user:
      recipes = Recipe.objects.filter(bookmark__chef=user)
      serialized = RecipeSerializer(recipes, many=True)
      return JsonResponse(serialized.data, safe=False)
    else:
      return Response("Error")

class AddRecipe(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if request.POST.get('edit'):
      print(request.POST.get('edit'))
      recipe = Recipe.objects.get(slug=request.POST.get('edit'), chef=user)
      form = RecipeForm(request.POST, instance=recipe)
    else:
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

class BookmarkRecipe(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    recipe = Recipe.objects.get(slug=request.POST.get('slug'), chef__username=request.POST.get('username'))

    try:
      # remove the bookmark
      bookmark = Bookmark.objects.get(chef=user, recipe=recipe)
      bookmark.delete()
      return Response(True)
    except Bookmark.DoesNotExist:
      # add the bookmark
      if recipe and user:
        Bookmark.objects.create(chef=user, recipe=recipe)
        return Response(True)
      else:
        return Response(False)