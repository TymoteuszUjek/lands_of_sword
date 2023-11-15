from django.db import models

class Enemy(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    enemy_class = models.CharField(max_length=100)
    enemy_race = models.CharField(max_length=100)
    hp = models.PositiveIntegerField()
    damage = models.PositiveIntegerField()
    strength = models.PositiveIntegerField(default=10)
    intelligence = models.PositiveIntegerField(default=10)
    constitution = models.PositiveIntegerField(default=10)
    dexterity = models.PositiveIntegerField(default=10)
    luck = models.PositiveIntegerField(default=10)
    wisdom = models.PositiveIntegerField(default=10)
    physical_res = models.PositiveIntegerField(default=10)
    magic_res = models.PositiveIntegerField(default=10)
    max_gold = models.PositiveIntegerField(default=10)
    min_gold = models.PositiveIntegerField(default=1)
    max_exp = models.PositiveIntegerField(default=10)
    min_exp = models.PositiveIntegerField(default=1)
    battle_duration = models.PositiveIntegerField(default=60) # Default battle duration is 60 seconds