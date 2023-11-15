from django.urls import path
from . import views

app_name = 'Items'
urlpatterns = [
    path('item_list/', views.item_list, name='item_list'),
]