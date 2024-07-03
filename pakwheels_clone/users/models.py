from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_num = models.IntegerField(blank=True,null=True)
