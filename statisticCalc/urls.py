from django.urls import path
from . import views

urlpatterns = [
  path("generate-excel/", views.controller_generate_excel, name="generate-excel"),
  path("get-file/", views.get_file, name="get-file")
]