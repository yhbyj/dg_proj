from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    path('books/', views.Book.as_view()),
    path('books/(?P<pk>.*)/', views.Book.as_view()),
    path('users/', views.User.as_view()),
    path('users/(?P<pk>.*)', views.User.as_view()),
]
