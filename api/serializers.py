from rest_framework import serializers
from api.models import Recipe
from django.contrib.auth.models import User

class RecipeSerializer(serializers.ModelSerializer):
  username = serializers.CharField(source='chef.username', read_only=True)

  class Meta:
    model = Recipe
    fields = ['title', 'slug', 'recipe', 'image', 'username']

