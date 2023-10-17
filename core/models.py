import uuid
from datetime import timedelta
from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
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
    forget_password_key = models.CharField(max_length=8, blank=True, null=True)
    key_expiry = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    def generate_forget_password_key(self):
        key = randint(100000, 999999)
        self.set_password(str(key))
        self.key_expiry = timezone.now() + timedelta(minutes=15)
        self.save()
        return key
