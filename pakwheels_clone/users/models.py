from django.contrib import auth
from django.contrib.auth.models import User
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    phone_num = models.IntegerField(blank=True,null=True)