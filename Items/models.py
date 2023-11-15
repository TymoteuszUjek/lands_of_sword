from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Item(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1, validators=[
        MinValueValidator(1), MaxValueValidator(100)])
    hp = models.IntegerField(default=1)
    base_hp = models.IntegerField(default=1)
    item_type = models.CharField(max_length=20)
    damage = models.IntegerField(default=1)
    base_damage = models.IntegerField(default=1)
    
    strength = models.IntegerField(default=1)
    base_strength = models.IntegerField(default=1)
    
    intelligence = models.IntegerField(default=1)
    base_intelligence = models.IntegerField(default=1)
    
    constitution = models.IntegerField(default=1)
    base_constitution = models.IntegerField(default=1)
    
    dexterity = models.IntegerField(default=1)
    base_dexterity = models.IntegerField(default=1)
    
    luck = models.IntegerField(default=1)
    base_luck = models.IntegerField(default=1)
    
    wisdom = models.IntegerField(default=1)
    base_wisdom = models.IntegerField(default=1)
    

    rarity = models.CharField(max_length=20)
    
    price = models.IntegerField(default=1)
    base_price = models.IntegerField(default=1)
    
    physical_res = models.PositiveIntegerField(default=10)
    base_physical_res = models.IntegerField(default=1)
    
    magic_res = models.PositiveIntegerField(default=10)
    base_magic_res = models.IntegerField(default=1)
    
    
    enhancement_level = models.IntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(20)])
    enhancement_cost = models.IntegerField(default=1)
    base_enhancement_cost = models.IntegerField(default=1)
    
    shop_type = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name