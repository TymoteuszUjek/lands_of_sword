from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    enemies_to_defeat = models.PositiveIntegerField(default=0)
    gold_to_earn = models.PositiveIntegerField(default=0)
    players_to_defeat = models.PositiveIntegerField(default=0)
    gold_reward = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.task_name}"