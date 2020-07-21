from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<slug>", views.single_page, name="single_page"),
    path("search", views.search_results, name="search"),
    path("create", views.create_page, name="create"),
]
