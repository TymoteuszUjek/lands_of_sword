from django.urls import path
from . import views

app_name = 'Tavern'
urlpatterns = [
    path('task_master/', views.task_master, name='task_master'),
    path('activate_task/<int:task_id>/', views.activate_task, name='activate_task'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('claim_reward/<int:task_id>/', views.claim_reward, name='claim_reward'),
    path('reset_tasks/', views.reset_tasks, name='reset_tasks'),  # Nowa ścieżka
]
