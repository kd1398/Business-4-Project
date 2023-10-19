import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

UserModel = get_user_model()


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.SlugField(blank=False, null=False)

    def __str__(self):
        return self.name


class FileData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    data = models.JSONField(blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
