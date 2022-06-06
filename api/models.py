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

    class Meta:
        constraints = [models.UniqueConstraint(fields=['chef', 'slug'], name='unique_slug_per_chef')]
        ordering = ['title']

class Bookmark(models.Model):
    chef = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class Chef_Settings(models.Model):
    chef = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    browsable_recipes = models.IntegerField()