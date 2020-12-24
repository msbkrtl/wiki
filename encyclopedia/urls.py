from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("newpage", views.new, name="new"),
    path("random", views.randomPage, name="randomPage"),
    path("error/<str:errorName>", views.error, name="error"),
    path("learning/<int:ids>", views.learning, name="learning"),
    path("edit/<str:entry>", views.edit, name="edit"),
]
