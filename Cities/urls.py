from django.urls import path
from . import views

app_name = 'Cities'

urlpatterns = [
    path('cities/', views.cities, name='cities'),
]
