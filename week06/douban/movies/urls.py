from django.urls import path

from . import views


urlpatterns = [
    path("movies/", views.index, name="movies"),
    path("movies/<int:pk>/", views.movie, name="movie"),
]
