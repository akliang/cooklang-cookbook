from django.urls import path

from api import views
from api.views.core import MyBookmarks

urlpatterns = [
  path('api_login/', views.LoginTokenAuth.as_view(), name='api_login'),
  path('api_register/', views.RegisterAccount.as_view(), name='api_register'),
  path('api_delete/', views.DeleteAccount.as_view(), name='api_delete'),
  path('api_changepw/', views.ChangeAccountPassword.as_view(), name='api_changepw'),
  path('view/<str:username>/<str:slug>', views.RecipeView.as_view(), name='view_recipe'),
  path('view_by_token/', views.GetRecipeWithToken.as_view(), name='get_recipe_with_token'),
  path('view/', views.MyRecipes.as_view(), name='my_recipes'),
  path('add/', views.AddRecipe.as_view(), name='add_recipe'),
  path('add_desktop/', views.AddRecipeDesktop.as_view(), name='add_recipe'),
  path('delete/', views.DeleteRecipe.as_view(), name='delete_recipe'),
  path('bookmark/', views.BookmarkRecipe.as_view(), name='bookmark_recipe'),
  path('view_bookmarks/', views.MyBookmarks.as_view(), name='my_bookmarks'),
  # path('export/', views.ExportRecipes.as_view(), name='export_recipes'),
]