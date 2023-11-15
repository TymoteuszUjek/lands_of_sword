from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class CharacterClass(models.Model):
    class_choices = (
        ('Knight', 'Knight'),
        ('Thief', 'Thief'),
        ('Wizard', 'Wizard'),
        ('Cleric', 'Cleric'),
        ('Ranger', 'Ranger'),
        ('Paladin', 'Paladin'),
        ('Barbarian', 'Barbarian'),
        ('Druid', 'Druid'),
        ('Bard', 'Bard'),
        ('Monk', 'Monk'),
        ('Necromancer', 'Necromancer'),
    )
    name = models.CharField(max_length=100, choices=class_choices)

    def __str__(self):
        return self.name


class CharacterRace(models.Model):
    race_choices = (
        ('Human', 'Human'),
        ('Elf', 'Elf'),
        ('Dwarf', 'Dwarf'),
        ('Orc', 'Orc'),
        ('Halfling', 'Halfling'),
        ('Centaur', 'Centaur'),
        ('Half-elf', 'Half-Elf'),
        ('Half-orc', 'Half-Orc'),
        ('Minotaur', 'Minotaur'),
        ('Lizardfolk', 'Lizardfolk'),
        ('Dragonborn', 'Dragonborn'),
        ('Sylvari', 'Sylvari'),
    )
    name = models.CharField(max_length=100, choices=race_choices)

    def __str__(self):
        return self.name


class Character(models.Model):
    last_purchase_time = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1, validators=[
                                MinValueValidator(1), MaxValueValidator(100)])
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    character_race = models.ForeignKey(CharacterRace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(max_length=20, choices=(('Female', 'Female'), ('Male', 'Male')))
    hp = models.PositiveIntegerField(default=200)
    damage = models.PositiveIntegerField(default=20)
    strength = models.PositiveIntegerField(default=20)
    intelligence = models.PositiveIntegerField(default=20)
    constitution = models.PositiveIntegerField(default=20)
    dexterity = models.PositiveIntegerField(default=20)
    luck = models.PositiveIntegerField(default=20)
    wisdom = models.PositiveIntegerField(default=20)
    skill_points = models.PositiveIntegerField(default=0)
    experience_points = models.PositiveIntegerField(default=0)
    physical_res = models.PositiveIntegerField(default=20)
    magic_res = models.PositiveIntegerField(default=20)
    gold = models.PositiveIntegerField(default=0)
    collected_gold = models.PositiveIntegerField(default=0)
    killed_monsters = models.PositiveIntegerField(default=0)
    killed_players = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.character_class}, Level {self.level})"

def calculate_experience_for_next_level(current_level):
    experience_needed = 500  

    while current_level > 1:
        experience_needed *= 1.35  
        current_level -= 1

    return int(experience_needed)
