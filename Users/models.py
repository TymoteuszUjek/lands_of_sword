from django.contrib.auth.models import User
from django.db import models
from Team.models import Character

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

