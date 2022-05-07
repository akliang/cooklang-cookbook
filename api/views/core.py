import re
import zipfile
import tempfile
from pathlib import Path

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

class DeleteRecipe(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    recipe = Recipe.objects.get(slug=request.POST.get('slug'), chef=user)

    if recipe:
      recipe.delete()
      return Response(True)
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