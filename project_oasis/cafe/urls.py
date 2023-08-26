from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #path('recommended', .as_view()),
    path('recommend/keyword', views.recommend_cafes_base_keyword),
    path('recommend/rating', views.recommend_cafes_base_rating),
]
