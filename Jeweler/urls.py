from django.urls import path
from . import views

app_name = 'Jeweler'

urlpatterns = [
    path('jeweler/', views.jeweler, name='jeweler'),
]
