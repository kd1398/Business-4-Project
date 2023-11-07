from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import CustomUserRoles

UserModel = get_user_model()

# Register your models here.


class UserModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserModel, UserModelAdmin)
admin.site.register(CustomUserRoles)
