from django.urls import path
from . import views

app_name = 'Fight'
urlpatterns = [
    path('battle/', views.battle, name='battle'),
    path('countdown/', views.countdown, name='countdown'),
    path('fight_selector/', views.fight_selector, name='fight_selector'),
]