from django.urls import path
from . import views

app_name = 'Team'
urlpatterns = [
    path('create_character/', views.create_character, name='create_character'),
    path('character_list/', views.character_list, name='character_list'),
]
