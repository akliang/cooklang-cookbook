from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chef(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  email = models.CharField(max_length=255)
  last_login = models.DateTimeField(auto_now=True)
