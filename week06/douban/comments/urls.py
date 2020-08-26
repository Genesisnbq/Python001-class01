from django.urls import path
from . import views


urlpatterns = [
    path('index', views.comment),
    path('', views.comment),
]

