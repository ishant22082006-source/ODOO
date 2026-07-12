from django.urls import path
from . import views

urlpatterns = [
    path("", views.maintenance_list, name="maintenance_list"),
    path("add/", views.maintenance_create, name="maintenance_create"),
    path(
        "<int:pk>/close/",
        views.maintenance_close,
        name="maintenance_close",
    ),
]