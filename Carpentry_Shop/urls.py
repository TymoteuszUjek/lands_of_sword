from django.urls import path
from . import views

app_name = 'Carpentry_Shop'

urlpatterns = [
    path('carpentry_shop/', views.carpentry_shop, name='carpentry_shop'),
]
