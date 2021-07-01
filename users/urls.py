"""Definiuje wzorce adresow URL dla aplikacji users."""

from django import urls
from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    #Dolaczanie domyslnych adresow URL uwierzytelniania
    path('', include('django.contrib.auth.urls')),

    #Strona rejestracji 
    path('register/', views.register, name='register'),
]