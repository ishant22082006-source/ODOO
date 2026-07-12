from django.urls import path
from . import views

urlpatterns = [
    path("", views.fuel_list, name="fuel_list"),
    path("add/", views.fuel_create, name="fuel_create"),
]