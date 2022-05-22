import re
import zipfile
import tempfile
from pathlib import Path
from collections import Counter
import operator

from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

from api.forms import RecipeForm
from api.helpers.cooklang import cooklang_processor as clprocess
from api.views.authentication import lookup_user_by_api, parse_apikey_from_header
from api.models import Recipe, Bookmark
from api.serializers import RecipeSerializer

import logging
logger = logging.getLogger(__name__)

class RecipeView(APIView):
  authentication_classes = ()
  permission_classes = (AllowAny,)

  def get(self, request, *args, **kw):
    try:
      recipe = Recipe.objects.get(slug=kw['slug'], chef__username=kw['username'])
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

      return Response({'title': recipe.title, 'ingredients': proc_recipe['ingredients'], 'recipe': proc_recipe['recipe'], 'edit': edit, 'bookmarked': bookmarked, 'image': recipe.image})
    except Recipe.DoesNotExist:
      logger.info(f"{self.__class__.__name__} - Invalid recipe request for chef \"{kw['username']}\" and slug \"{kw['slug']}\"")
      return Response(status=status.HTTP_400_BAD_REQUEST)

class GetRecipeWithToken(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    try:
      recipe = Recipe.objects.get(slug=request.POST.get('slug'), chef=user)
      return JsonResponse(RecipeSerializer(recipe).data)
    except Recipe.DoesNotExist:
      apikey = parse_apikey_from_header(request)
      logger.warning(f"{self.__class__.__name__} - Invalid recipe request for API key {apikey} and slug \"{request.POST.get('slug')}\"")
      return Response(status=status.HTTP_400_BAD_REQUEST)

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
      apikey = parse_apikey_from_header(request)
      logger.warning(f"{self.__class__.__name__} - Invalid home page (my recipes list) request for API key {apikey}")
      return Response(status=status.HTTP_401_UNAUTHORIZED)

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
      apikey = parse_apikey_from_header(request)
      logger.warning(f"{self.__class__.__name__} - Invalid bookmark page request for API key {apikey}")
      return Response(status=status.HTTP_401_UNAUTHORIZED)

# TODO: convert this to cooklang ingester
class AddRecipe(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if request.POST.get('edit'):
      recipe = Recipe.objects.get(slug=request.POST.get('edit'), chef=user)
      form = RecipeForm(request.POST, instance=recipe)
    else:
      form = RecipeForm(request.POST)

    # write the form data to cook file
    if form.is_valid():
      # if the title hits integrity error, append a number to it and try again... until it works
      cnt = 0
      while True:
        title = form.cleaned_data['title']

        if cnt != 0:
          title = f"{title} {cnt}"

        # build the slug, first remove all non-alphanumeric characters
        slug = re.sub('[^a-zA-Z0-9 ]', '', title)
        slug = re.sub('\s', '-', slug)
        slug = slug.lower()

        obj = form.save(commit=False)
        obj.chef = user
        obj.slug = slug

        try:
          obj.save()
          return Response({
            'username': user.username,
            'slug': slug
          }, status=status.HTTP_201_CREATED)
        except IntegrityError:
          cnt += 1
          # return Response("Title is same or too similar to another recipe.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
      apikey = parse_apikey_from_header(request)
      logger.warning(f"{self.__class__.__name__} - Invalid add recipe request for API key {apikey}")
      return Response(form.errors, status=status.HTTP_401_UNAUTHORIZED)

class AddRecipeDesktop(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)

    # rebuild the ingredientname and ingredientqty arrays
    # (they get broken up by expressJS... not sure how to fix it right now)
    ingredients = {}
    for val in request.POST:
      if 'ingredientname' in val:
        # strip whitespace from the ingredient
        ingredientname = request.POST[val].lstrip()
        ingredientname = ingredientname.rstrip()

        # find and format the ingredient quantity
        idx = val.replace('ingredientname[', '')
        idx = idx.replace(']', '')
        ingredientqty = request.POST[f"ingredientqty[{idx}]"]
        # replace the first whitespace with percent sign (per cooklang spec)
        ingredientqty = ingredientqty.replace(" ", "%", 1)

        ingredients[ingredientname] = ingredientqty

    # make a copy of request.POST so it's mutable (need to modify "recipe")
    post = request.POST.copy()

    # parse through all the ingredients and cooklang-decorate the recipe
    for ingredientname, ingredientqty in ingredients.items():
      print(ingredientname)
      # find first instance of ingredient in the recipe
      post['recipe'] = post['recipe'].replace(ingredientname, f"@{ingredientname}{{{ingredientqty}}}", 1)

    # validate the recipe structure
    if post.get('edit'):
      recipe = Recipe.objects.get(slug=post.get('edit'), chef=user)
      form = RecipeForm(post, instance=recipe)
    else:
      form = RecipeForm(post)

    # write the form data to cook file
    if form.is_valid():
      # if the slug hits integrity error, append a number to title and try again... until it works
      cnt = 1
      while True:
        title = form.cleaned_data['title']

        # don't want to append the number on first try
        if cnt != 1:
          title = f"{title} {cnt}"

        # build the slug, first remove all non-alphanumeric characters
        slug = re.sub('[^a-zA-Z0-9 ]', '', title)
        slug = re.sub('\s', '-', slug)
        slug = slug.lower()

        obj = form.save(commit=False)
        obj.chef = user
        obj.slug = slug

        try:
          obj.save()
          return Response({
            'username': user.username,
            'slug': slug
          }, status=status.HTTP_201_CREATED)
        except IntegrityError:
          cnt += 1
    else:
      apikey = parse_apikey_from_header(request)
      logger.warning(f"{self.__class__.__name__} - Invalid add recipe request for API key {apikey}")
      return Response(form.errors, status=status.HTTP_401_UNAUTHORIZED)

class DeleteRecipe(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    recipe = Recipe.objects.get(slug=request.POST.get('slug'), chef=user)

    if recipe:
      img_name = recipe.image
      recipe.delete()
      return Response(img_name)
    else:
      apikey = parse_apikey_from_header(request)
      logger.warning(f"{self.__class__.__name__} - Invalid delete recipe request for API key {apikey}")
      return Response(status=status.HTTP_401_UNAUTHORIZED)

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
        apikey = parse_apikey_from_header(request)
        logger.warning(f"{self.__class__.__name__} - Invalid bookmark recipe request for API key {apikey}, chef \"{kw['username']}\" and slug \"{kw['slug']}\"")
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class WhatCanICook(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if not user:
      apikey = parse_apikey_from_header(request)
      logger.warning(f"{self.__class__.__name__} - Invalid my_ingredients request for API key {apikey}")
      return Response(status=status.HTTP_401_UNAUTHORIZED)

    # step through each recipe and parse the cooklang
    recipes = Recipe.objects.filter(chef=user)
    ingredient_counter = Counter()
    for recipe in recipes:
      proc_recipe = clprocess(recipe.recipe)
      # [my_ingredients[i] += 1 for i in proc_recipe['ingredients']]
      for key in proc_recipe['ingredients']:
        ingredient_counter[key] += 1

    my_ingredients = dict( sorted(ingredient_counter.items(), key=operator.itemgetter(1), reverse=True))

    return JsonResponse(my_ingredients)
    


    # try:
    #   # remove the bookmark
    #   bookmark = Bookmark.objects.get(chef=user, recipe=recipe)
    #   bookmark.delete()
    #   return Response(True)
    # except Bookmark.DoesNotExist:
    #   # add the bookmark
    #   if recipe and user:
    #     Bookmark.objects.create(chef=user, recipe=recipe)
    #     return Response(True)
    #   else:
    #     apikey = parse_apikey_from_header(request)
    #     logger.warning(f"{self.__class__.__name__} - Invalid bookmark recipe request for API key {apikey}, chef \"{kw['username']}\" and slug \"{kw['slug']}\"")
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

# class ExportRecipes(APIView):
#   authentication_classes = [TokenAuthentication]
#   permission_classes = [IsAuthenticated]

#   def post(self, request, *args, **kw):
#     user = lookup_user_by_api(request)
#     recipeset = Recipe.objects.filter(chef=user)
    
#     # start the zipfile handle
#     response = HttpResponse(content_type='application/zip')
#     zf = zipfile.ZipFile(response, 'w')
#     for recipe in recipeset:
#         cl_recipe = f">> Title: {recipe.title}\n\n{recipe.recipe}"
#         zf.writestr(recipe.slug, cl_recipe)

#     response['Content-Disposition'] = f'attachment; filename=testing.zip'
#     return response