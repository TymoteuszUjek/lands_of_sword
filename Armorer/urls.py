from django.urls import path
from . import views

app_name = 'Armorer'

urlpatterns = [
    path('armorer/', views.armorer, name='armorer'),
]
