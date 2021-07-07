"""Definiuje wzorce adresów URL dla learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
	#strona glowna.
	path('', views.index, name='index'),

	#wyswietlanie wszystkich tematow.
	path('topics/', views.topics, name = 'topics'),

	#Strona szczegółowa dotycząca pojedynczego tematu.
	path('topics/<int:topic_id>/', views.topic, name='topic'),

	#Strona przeznaczona do dodawania nowego tematu.
	path('new_topic/', views.new_topic, name='new_topic'),
	
	#Strona przeznaczona do dodawania nowego wpisu.
	path('new_entry/<int:topic_id>)/', views.new_entry, name ='new_entry'),

	#Strona przeznaczona do edycji wpisu
	path('edit_entry/<int:entry_id>/', views.edit_entry, name ='edit_entry'),
	
	#strona przeznaczona do usuwania wpisu
	path('topics/<int:entry_id>/remove_entry/', views.remove_entry, name='remove_entry'),

	#strona przeznaczona do usuwania tematu
	path('topics/<int:topic_id>/remove_topic/', views.remove_topic, name="remove_topic"),
	
]