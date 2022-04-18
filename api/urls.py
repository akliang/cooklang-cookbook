from django.urls import path

from api import views

urlpatterns = [
  # path('', views.index, name='index'),
  path('api_login/', views.LoginTokenAuth.as_view(), name='api_login'),
  # path('login/', views.login, name='login'),
  # path('api_login/', views.ApiLogin.as_view(), name='api_login'),
  # path('logout/', views.logout, name='logout'),
  # path('register/', views.register, name='register'),
  # path('recipe/', views.recipe, name='recipe'),
  # path('v/<str:username>/<str:filename>', views.view, name='view'),
  # path('view/<str:user>/', views.MyRecipesView.as_view(), name='MyRecipesView'),
  path('view/<str:user>/<str:recipe>', views.RecipeView.as_view(), name='RecipeView'),
  # path('view/<str:user>/<str:recipe>', views.recipe_view, name='temp'),
  path('view/', views.MyRecipes.as_view(), name='MyRecipes'),
  path('add/', views.AddRecipe.as_view(), name='Addrecipe'),
]