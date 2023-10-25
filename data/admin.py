from django.contrib import admin
from .models import Category, FileData, Module
# Register your models here.

admin.site.register(Category)
admin.site.register(FileData)
admin.site.register(Module)
