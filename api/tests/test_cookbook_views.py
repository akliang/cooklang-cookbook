#   path('view/<str:username>/<str:slug>', views.RecipeView.as_view(), name='view_recipe'),
#   path('view_by_token/', views.GetRecipeWithToken.as_view(), name='get_recipe_with_token'),
#   path('view/', views.MyRecipes.as_view(), name='my_recipes'),
#   path('add/', views.AddRecipe.as_view(), name='add_recipe'),
#   path('add_desktop/', views.AddRecipeDesktop.as_view(), name='add_recipe'),
#   path('delete/', views.DeleteRecipe.as_view(), name='delete_recipe'),
#   path('bookmark/', views.BookmarkRecipe.as_view(), name='bookmark_recipe'),
#   path('view_bookmarks/', views.MyBookmarks.as_view(), name='my_bookmarks'),
#   # path('export/', views.ExportRecipes.as_view(), name='export_recipes'),
#   path('whatcanicook/', views.WhatCanICook.as_view(), name='whatcanicook'),


from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class TestCookbookViews(TestCase):
  username = "testuser123456"
  username2 = "testuser123456789"
  password = "98vbzlkqb3lahsfdpo87"
  new_password = "98vbzlkqb3lahsfdpo87444"
  email = "test@test.com"

  def setUp(self):
    user = User.objects.create_user(username=self.username, password=self.password)

  def test_view(self):
    # without login

    # with login
    response = self.client.post('/api/api_login/', {'username': self.username, 'password': self.password})
    