import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    """Basic Info"""
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=False, unique=True, max_length=254, verbose_name="Email Address")

    '''Authentication'''
    jwt_token_key = models.CharField(max_length=12, default=get_random_string(length=12))

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

