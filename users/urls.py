"""Definiuje wzorce adresów URL dla aplikacji users."""

from django import urls
from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    #Dolaczanie domyślnych adresów URL uwierzytelniania
    path('', include('django.contrib.auth.urls')),

    #Strona rejestracji
    path('register/', views.register, name='register'),
    #strona edycji uzytkownika
    path('edit_profile/', views.edit_profile, name='edit_profile')
]