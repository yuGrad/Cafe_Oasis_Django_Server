from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('rating/create', views.create_cafe_rating_history),
    path('visit/create', views.create_cafe_visit_history),
]
