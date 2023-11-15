from django.urls import path
from . import views

app_name = 'Blacksmith'

urlpatterns = [
    path('blacksmith/', views.blacksmith, name='blacksmith'),
]
