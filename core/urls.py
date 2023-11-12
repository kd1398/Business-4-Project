from django.urls import path
from django.contrib.auth import views as auth_views
from core import views
# from .views import CustomPasswordResetView

urlpatterns = [
    path('get_users/', views.user_list),
    path('forget_password/', views.forget_password),
    path('create_user/', views.create_user),
    path('change_password/', views.change_password),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name='password_reset'),

    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
]
