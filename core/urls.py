from django.urls import path

from core import views

urlpatterns = [
    path('get_users/', views.user_list),
    path('forget_password/', views.forget_password),
    path('change_password/', views.change_password),
    path('add_new_user_role/', views.add_new_user_role),
    path('add_new_user/', views.add_new_user),
]
