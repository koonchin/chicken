from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
path("", views.dashboard, name="dashboard"),
path("dashboard/", views.dashboard, name="dashboard"),
path("insert/", views.insert, name="insert"),
path("edit/<id>", views.edit, name="edit"),
path("delete/<id>", views.deleteId, name="delete"),
path("share/<id>", views.sharePage, name="share"),
path("list/", views.listPage, name="list"),
path("open_file/<id>", views.open_file, name="open-file"),
path("view_file/<id>", views.view_file, name="view-file"),
]