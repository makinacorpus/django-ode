from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_provider = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
