from django.urls import path
from . import views

app_name = "file_manager"

urlpatterns = [
    path("", views.file_manager_list, name="file_manager_list"),
    path("", views.file_manager_list, name="list"),
]