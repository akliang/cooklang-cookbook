from operator import mod
from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    chef = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    tags = models.CharField(max_length=200, blank=True)
    recipe = models.TextField()
    image = models.CharField(max_length=200, blank=True)

class Bookmark(models.Model):
    chef = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)