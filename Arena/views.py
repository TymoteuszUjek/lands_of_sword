from django.shortcuts import render
from Team.models import Character
from random import choice
import math
import random

def enemy_select(request):
    user_character = Character.objects.get(user=request.user)
    min_level = max(1, user_character.level - 5)  # Minimum level for opponent
    max_level = user_character.level + 5  # Maximum level for opponent

    # Wybierz zapisanego przeciwnika lub wylosuj nowego
    selected_enemy_id = request.session.get('selected_enemy')
    if selected_enemy_id:
        enemies = Character.objects.get(pk=selected_enemy_id)
    else:
        # Losuj przeciwnika spośród odpowiednich poziomów i wyklucz aktualnie zalogowanego gracza
        enemies = choice(Character.objects.filter(level__gte=min_level, level__lte=max_level).exclude(pk=user_character.pk))

    # Zapisz wybranego przeciwnika w sesji
    request.session['selected_enemy'] = enemies.pk

    # Oblicz dane życiowe gracza i przeciwnika
    user_max_life = int(user_character.hp * ((1 + user_character.constitution * 0.1) * (1 + user_character.wisdom * 0.1)) / 10)
    enemy_max_life = int(enemies.hp * ((1 + enemies.constitution * 0.1) * (1 + enemies.wisdom * 0.1)) / 10)

    # Przekaz informacje o graczu i przeciwniku do szablonu
    context = {
        'user_character': user_character,
        'enemy_character': enemies,
        'user_max_life': user_max_life,
        'enemy_max_life': enemy_max_life,
    }

    return render(request, 'Arena/arena_select.html', context)



def fight(request):
    user_character = Character.objects.get(user=request.user)

    min_enemy_level = max(1, user_character.level - 5)  # Minimum level for opponent
    max_enemy_level = user_character.level + 5  # Maximum level for opponent

    # Wybierz zapisanego przeciwnika lub wylosuj nowego
    selected_enemy_id = request.session.get('selected_enemy')
    if selected_enemy_id:
        enemies = Character.objects.get(pk=selected_enemy_id)
    else:
        # Losuj przeciwnika spośród odpowiednich poziomów i wyklucz aktualnie zalogowanego gracza
        enemies = choice(Character.objects.filter(level__gte=min_enemy_level, level__lte=max_enemy_level).exclude(pk=user_character.pk))

    # Zapisz wybranego przeciwnika w sesji
    request.session['selected_enemy'] = enemies.pk

        
    user_max_life = int(user_character.hp * ((1 + user_character.constitution * 0.1) *
                                             (1 + user_character.wisdom * 0.1)) / 10)
    enemy_max_life = int(enemies.hp * ((1 + enemies.constitution * 0.1) *
                                            (1 + enemies.wisdom * 0.1)) / 10)


    enemy_life = enemy_max_life
    user_life = user_max_life
    if enemies == user_character:
        enemy_life = enemy_life/2
    battle_result = None
    
    earned_gold = 0  # Initialize the earned_gold variable
    earned_exp = 0  # Initialize the earned_exp variable

    user_damage_log = []
    enemy_damage_log = []

    while user_life > 0 and enemy_life > 0:
        user_hit_chance = (user_character.dexterity + user_character.luck) / 50
        user_crit_chance = user_character.luck / 100

        enemy_hit_chance = (enemies.dexterity + enemies.luck) / 20
        enemy_crit_chance = enemies.luck / 100

        user_damage = (( (user_character.damage * (user_character.strength + (user_character.strength * (10/(enemies.physical_res+enemies.constitution))))) + (user_character.damage * (user_character.intelligence + (user_character.intelligence * (10/(enemies.magic_res+ enemies.wisdom ))))) ) *  user_hit_chance * user_crit_chance ) / 10

        enemy_damage = (( (enemies.damage * (enemies.strength + (enemies.strength * (10/(user_character.physical_res+user_character.constitution))))) + (enemies.damage * (enemies.intelligence + (enemies.intelligence * (10/(user_character.magic_res+user_character.wisdom))))) ) *  enemy_hit_chance * enemy_crit_chance ) / 10
        if enemies == user_character:
            enemy_damage = enemy_damage/2
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
        
        # Increment earned_exp and earned_gold when the battle is won
        earned_exp += int(user_character.level * 100)
        earned_gold += int(user_character.level * 10)
        
        user_character.experience_points += earned_exp
        user_character.gold += earned_gold
        user_character.killed_players += 1
        user_character.collected_gold += earned_gold
        user_character.save()    
        
        
    total_user_damage = math.floor(sum(enemy_damage_log))
    total_enemy_damage = math.floor(sum(user_damage_log))    
    
    context = {
        'user_character': user_character,
        'enemies': enemies,
        'battle_result': battle_result,
        'user_health': user_health,
        'enemy_health': enemy_health,
        'total_user_damage': total_user_damage,
        'total_enemy_damage': total_enemy_damage,
        'enemy_damage_log': enemy_damage_log,
        'user_max_health': user_max_life,
        'enemy_max_health': enemy_max_life,
        'earned_gold': earned_gold,
        'earned_exp': earned_exp,
    }
    return render(request, 'Arena/arena_fight.html', context)