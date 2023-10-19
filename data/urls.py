from django.urls import path

from . import views

app_name = "data"

urlpatterns = [
    path('upload_file/', views.upload_file),
    path('get_file_categories/', views.get_file_categories),
    path('get_file_names/', views.get_file_names),
    path('get_file_data/', views.get_file_data)
]
