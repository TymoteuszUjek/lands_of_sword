
from django.shortcuts import render, redirect
import random
from random import choice
from Bots_Farm.models import Enemy
from Team.models import Character
import math
from django.contrib.sessions.models import Session
from django.utils import timezone
import datetime
from Inventory.models import InventoryItem
from Items.models import Item
from django.http import Http404

def countdown(request):
    min_level = request.GET.get('min_level')
    max_level = request.GET.get('max_level')

    if min_level is None or max_level is None:
        raise Http404("Invalid parameters")

    try:
        min_level = int(min_level)
        max_level = int(max_level)
    except ValueError:
        raise Http404("Invalid parameters")

    random_enemy = Enemy.objects.filter(level__gte=min_level, level__lte=max_level).order_by('?').first()

    
    user_id = request.user.id
    countdown_active_key = f'countdown_active_{user_id}'
    selected_enemy_key = f'selected_enemy_{user_id}'
    battle_start_time_key = f'battle_start_time_{user_id}'

    request.session[countdown_active_key] = True

    if random_enemy is None:
        raise Http404("No enemies in the selected range")

    request.session[selected_enemy_key] = random_enemy.id

    selected_enemy_id = request.session.get(selected_enemy_key)
    if selected_enemy_id:
        random_enemy = Enemy.objects.get(pk=selected_enemy_id)
        remaining_time = random_enemy.battle_duration
    else:
        remaining_time = 60

    time_to_display = int(remaining_time/60)

    if battle_start_time_key in request.session:
        battle_start_time_str = request.session[battle_start_time_key]
        battle_start_time = datetime.datetime.strptime(battle_start_time_str, "%Y-%m-%d %H:%M:%S.%f%z")

        current_time = timezone.now()
        time_elapsed = (current_time - battle_start_time).total_seconds()

        if time_elapsed < remaining_time:
            remaining_time = remaining_time - int(time_elapsed)

        request.session[battle_start_time_key] = str(timezone.now())

    context = {
        'remaining_time': remaining_time,
        'random_enemy': random_enemy,
        'time_to_display': time_to_display,
    }
    return render(request, 'Fight/countdown.html', context)


def battle(request):
    user_id = request.user.id
    countdown_active_key = f'countdown_active_{user_id}'
    battle_start_time_key = f'battle_start_time_{user_id}'

    if battle_start_time_key not in request.session:
        request.session[countdown_active_key] = False
        request.session[battle_start_time_key] = str(timezone.now())

    user_character = Character.objects.get(user=request.user)

    selected_enemy_id = request.session.get(f'selected_enemy_{user_id}')
    if selected_enemy_id:
        random_enemy = Enemy.objects.get(pk=selected_enemy_id)
    else:
        random_enemy = choice(Enemy.objects.all())

    user_max_life = int(user_character.hp * ((1 + user_character.constitution * 0.1) *
                                             (1 + user_character.wisdom * 0.1)) / 10)
    enemy_max_life = int(random_enemy.hp * ((1 + random_enemy.constitution * 0.1) *
                                            (1 + random_enemy.wisdom * 0.1)) / 10)

    enemy_life = enemy_max_life
    user_life = user_max_life

    battle_result = None

    user_damage_log = []
    enemy_damage_log = []
    
    new_items = []
    item_message = ""
    earned_gold = 0
    earned_exp = 0

    while user_life > 0 and enemy_life > 0:
        user_hit_chance = (user_character.dexterity + user_character.luck) / 50
        user_crit_chance = user_character.luck / 100

        enemy_hit_chance = (random_enemy.dexterity + random_enemy.luck) / 20
        enemy_crit_chance = random_enemy.luck / 100

        
        user_damage = (( (user_character.damage * (user_character.strength + (user_character.strength * (10/(random_enemy.physical_res+random_enemy.constitution))))) + (user_character.damage * (user_character.intelligence + (user_character.intelligence * (10/(random_enemy.magic_res+ random_enemy.wisdom ))))) ) *  user_hit_chance * user_crit_chance ) / 10

        enemy_damage = (( (random_enemy.damage * (random_enemy.strength + (random_enemy.strength * (10/(user_character.physical_res+user_character.constitution))))) + (random_enemy.damage * (random_enemy.intelligence + (random_enemy.intelligence * (10/(user_character.magic_res+user_character.wisdom))))) ) *  enemy_hit_chance * enemy_crit_chance ) / 10

        enemy_life -= max(0, user_damage)
        user_life -= max(0, enemy_damage)

        user_damage_log.append(max(0, user_damage))
        enemy_damage_log.append(max(0, enemy_damage))

    if user_life <= 0 and enemy_life <= 0:
        battle_result = 'draw'
        user_health = 0
        enemy_health = 0
    elif user_life <= 0:
        battle_result = 'lose'
        user_health = 0
        enemy_health = max(0, enemy_life)
    else:
        battle_result = 'win'
        user_health = max(0, user_life)
        enemy_health = max(0, enemy_life)
        
        earned_gold = 0
        earned_exp = 0
        
        earned_exp += random.randint(random_enemy.min_exp, random_enemy.max_exp)
        earned_gold += random.randint(random_enemy.min_gold, random_enemy.max_gold)
        
        user_character.experience_points += earned_exp
        user_character.gold += earned_gold
        
        user_character.killed_players += 1
        user_character.collected_gold += earned_gold
        
        user_character.save()
        
        if battle_result == 'win':
            
            rarity_choices = ['Common', 'Uncommon', 'Rare', 'Legendary']
            rarity_probabilities = [0.7, 0.2, 0.08, 0.02]  

            
            item_rarity = random.choices(rarity_choices, rarity_probabilities)[0]

            items_with_rarity = Item.objects.filter(rarity=item_rarity)
            if items_with_rarity.exists():
                random_item = random.choice(items_with_rarity)
            else:
                random_item = random.choice(Item.objects.all())
            existing_item = InventoryItem.objects.filter(user=request.user, item=random_item).first()

            if existing_item:
                item_message = "You already have this item."
            else:
                new_inventory_item = InventoryItem(user=request.user, item=random_item)
                new_inventory_item.item_type += random_item.item_type
                new_inventory_item.shop_type += random_item.shop_type
                new_inventory_item.name += random_item.name
                new_inventory_item.level += random_item.level
                new_inventory_item.hp += random_item.hp
                new_inventory_item.damage += random_item.damage
                new_inventory_item.strength += random_item.strength
                new_inventory_item.intelligence += random_item.intelligence
                new_inventory_item.constitution += random_item.constitution
                new_inventory_item.dexterity += random_item.dexterity
                new_inventory_item.luck += random_item.luck
                new_inventory_item.wisdom += random_item.wisdom
                new_inventory_item.rarity += random_item.rarity
                new_inventory_item.price += random_item.price
                new_inventory_item.physical_res += random_item.physical_res
                new_inventory_item.magic_res += random_item.magic_res
                new_inventory_item.enhancement_level += random_item.enhancement_level
                new_inventory_item.enhancement_cost += random_item.enhancement_cost
                new_inventory_item.save()
                item_message = f"You received a {random_item.name} of {item_rarity} rarity."

    total_user_damage = math.floor(sum(enemy_damage_log))
    total_enemy_damage = math.floor(sum(user_damage_log))

    if battle_result == 'win':
        new_items = InventoryItem.objects.filter(user=request.user, item__name=random_item.name)
    else:
        new_items = []
        
    request.session[countdown_active_key] = False

    context = {
        'user_character': user_character,
        'random_enemy': random_enemy,
        'battle_result': battle_result,
        'user_health': user_health,
        'enemy_health': enemy_health,
        'total_user_damage': total_user_damage,
        'total_enemy_damage': total_enemy_damage,
        'enemy_damage_log': enemy_damage_log,
        'user_max_health': user_max_life,
        'enemy_max_health': enemy_max_life,
        'new_items': new_items,
        'item_message': item_message,
        'earned_gold': earned_gold,
        'earned_exp': earned_exp,
    }
    return render(request, 'Fight/battle.html', context)


def fight_selector(request):
    return render (request, 'Fight/fight_selector.html')
