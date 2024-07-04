from django.db import models
from django.contrib.auth.models import AbstractUser

from . user_manager import UserManager


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email = None
    username = None
    
    USERNAME_FIELD = 'phone_number'
    objects = UserManager()
