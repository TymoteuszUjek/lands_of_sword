from django.urls import path
from . import views

app_name = 'Clothier'

urlpatterns = [
    path('clothier/', views.clothier, name='clothier'),
]
