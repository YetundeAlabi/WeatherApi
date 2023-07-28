from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class User(AbstractUser):
    verification_code = models.CharField(max_length=5, blank=True, null=True)