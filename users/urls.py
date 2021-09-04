"""Definiuje wzorce adresów URL dla aplikacji users."""

# from django import urls
from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    # Dolaczanie domyślnych adresów URL uwierzytelniania
    path('', include('django.contrib.auth.urls')),

    # Strona rejestracji
    path('register/', views.register, name='register'),
    # strona edycji uzytkownika
    path('edit_settings/', views.edit_settings, name='edit_settings'),
    path('profile/<int:pk>/', views.profile, name= "profile"),
    path('profile/edit/<int:pk>', views.edit_profile, name='edit_profile'),
    path('profile/new_profile', views.new_profile, name= "new_profile"),

]