from django.urls import path
from . import views

app_name = 'Inventory'
urlpatterns = [
    path('equipment/', views.inventory, name='equipment'),
]
