from django.urls import path
from . import views

app_name = 'Boss_Fight'
urlpatterns = [
    
    path('regions/', views.regions, name='regions'),
]