from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('recommended', .as_view()),
    path('', views.CafeView.as_view()),
    path('/recommend/keyword', views.RecommendCafeKeywordView.as_view()),
    path('/recommend/rating', views.RecommendCafeRatingView.as_view()),
    
]
