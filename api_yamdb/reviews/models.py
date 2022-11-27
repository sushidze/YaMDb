from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Administrator'),
]


class User(AbstractUser):
    bio = models.CharField(max_length=250, null=True, blank=True)
    role = models.CharField(max_length=20, default='user', choices=ROLES)
    confirmation_code = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True)
