from django.urls import path

from api import views

urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('register/', views.register, name='register'),
  path('recipe/', views.recipe, name='recipe'),
  path('v/<str:username>/<str:filename>', views.view, name='view'),
]