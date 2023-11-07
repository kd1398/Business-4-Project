from django.contrib import admin
from .models import Category, FileData, Module, FileDataHistory


# Register your models here.


class FileDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Category)
admin.site.register(FileData, FileDataAdmin)
admin.site.register(FileDataHistory)
admin.site.register(Module)
