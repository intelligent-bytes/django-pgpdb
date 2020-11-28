from django.urls import path

from . import views

app_name = 'pgpdb'

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("lookup/", views.lookup, name="lookup"),
]
