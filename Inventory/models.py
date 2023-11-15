from django.db import models
from enum import Enum
from Team.models import User, Character
from Items.models import Item
from django.core.validators import MaxValueValidator, MinValueValidator

class ItemCategory(Enum):
    MAIN_HAND = 'Main Hand'
    OFF_HAND = 'Off Hand'
    HEAD = 'Head'
    SHOULDER = 'Shoulder'
    CHEST = 'Chest'
    HANDS = 'Hands'
    FEET = 'Feet'
    NECK = 'Neck'
    CAPE = 'Cape'
    RING = 'Ring'
    CHARM = 'Charm'

class InventoryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    equipped = models.BooleanField(default=False)
    item_type = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=100, default='')
    level = models.IntegerField(default=1, validators=[
        MinValueValidator(1), MaxValueValidator(100)])
    hp = models.IntegerField(default=0)
    damage = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    intelligence = models.IntegerField(default=0)
    constitution = models.IntegerField(default=0)
    dexterity = models.IntegerField(default=0)
    luck = models.IntegerField(default=0)
    wisdom = models.IntegerField(default=0)
    rarity = models.CharField(max_length=20, default='')
    price = models.IntegerField(default=0)
    physical_res = models.PositiveIntegerField(default=0)
    magic_res = models.PositiveIntegerField(default=0)
    enhancement_level = models.IntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(20)])
    enhancement_cost = models.IntegerField(default=0)
    shop_type = models.CharField(max_length=20, blank=True)
    
    
    def apply_upgraded_stats(self):
        enhancement_multiplier = 1.015
        self.damage = int(self.damage * enhancement_multiplier)
        self.hp = int(self.hp * enhancement_multiplier)
        self.strength += int(self.strength * enhancement_multiplier)
        self.intelligence += int(self.intelligence * enhancement_multiplier)
        self.constitution += int(self.constitution * enhancement_multiplier)
        self.dexterity += int(self.dexterity * enhancement_multiplier)
        self.luck += int(self.luck * enhancement_multiplier)
        self.wisdom += int(self.wisdom * enhancement_multiplier)
        self.price += int(self.price * enhancement_multiplier)
        self.physical_res += int(self.physical_res * enhancement_multiplier)
        self.magic_res += int(self.magic_res * enhancement_multiplier)
        self.enhancement_cost += int(self.enhancement_cost * enhancement_multiplier)
        self.enhancement_level += 1
        self.save()

    def apply_item_stats(self):
        character = Character.objects.get(user=self.user)  
        if self.equipped == True :
            character.strength += self.strength
            character.intelligence += self.intelligence
            character.constitution += self.constitution
            character.dexterity += self.dexterity
            character.luck += self.luck
            character.wisdom += self.wisdom
            character.physical_res += self.physical_res
            character.magic_res += self.magic_res
            character.save()

    def remove_item_stats(self):
        character = Character.objects.get(user=self.user)
        if self.equipped == False :
            character.strength -= self.strength
            character.intelligence -= self.intelligence
            character.constitution -= self.constitution
            character.dexterity -= self.dexterity
            character.luck -= self.luck
            character.wisdom -= self.wisdom
            character.physical_res -= self.physical_res
            character.magic_res -= self.magic_res
            character.save()

    def __str__(self):
        return f"{self.user.username}'s {self.name}"