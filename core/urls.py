from django.urls import path

from core import views

urlpatterns = [
    path('get_users/', views.user_list),
    path('forget_password/', views.forget_password),
    path('create_user/', views.create_user),
    path('change_password/', views.change_password),
]

