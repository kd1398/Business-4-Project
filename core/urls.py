from django.urls import path

from core import views

urlpatterns = [
    path('get_users/', views.user_list),
    path('create_user/', views.create_user)
]

