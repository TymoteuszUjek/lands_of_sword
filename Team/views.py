from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Character, calculate_experience_for_next_level
from .forms import CharacterForm
from django.shortcuts import get_object_or_404

def apply_class_stats(character):
    class_stats = {
        'Knight': {'hp': 100, 'strength': 10, 'intelligence': -5, 'constitution': 5, 'dexterity': -2, 'luck': -2, 'wisdom': -5, 'physical_res': 10, 'magic_res': -5},
        'Thief': {'hp': -20, 'strength': -2, 'intelligence': -2, 'constitution': -2, 'dexterity': 10, 'luck': 5, 'wisdom': -2, 'physical_res': 2, 'magic_res': 2},
        'Wizard': {'hp': -50, 'strength': -5, 'intelligence': 10, 'constitution': -4, 'dexterity': 3, 'luck': 2, 'wisdom': 5, 'physical_res': -5, 'magic_res': 10},
        'Cleric': {'hp': -30, 'strength': -7, 'intelligence': 8, 'constitution': -2, 'dexterity': 4, 'luck': 3, 'wisdom': 6, 'physical_res': -3, 'magic_res': 12},
        'Ranger': {'hp': -20, 'strength': -2, 'intelligence': 2, 'constitution': -2, 'dexterity': 10, 'luck': 3, 'wisdom': 2, 'physical_res': -1, 'magic_res': -1},
        'Paladin': {'hp': 50, 'strength': 5, 'intelligence': 5, 'constitution': 5, 'dexterity': 3, 'luck': -3, 'wisdom': 3, 'physical_res': 5, 'magic_res': 5},
        'Barbarian': {'hp': 50, 'strength': 15, 'intelligence': -10, 'constitution': 5, 'dexterity': 3, 'luck': 1, 'wisdom': -3, 'physical_res': -7, 'magic_res': -7},
        'Druid': {'hp': -50, 'strength': -5, 'intelligence': 10, 'constitution': -4, 'dexterity': 3, 'luck': 2, 'wisdom': 5, 'physical_res': -5, 'magic_res': 10},
        'Bard': {'hp': -30, 'strength': 3, 'intelligence': 3, 'constitution': -3, 'dexterity': 3, 'luck': 10, 'wisdom': 3, 'physical_res': 3, 'magic_res': 3},
        'Monk': {'hp': -20, 'strength': 7, 'intelligence': -4, 'constitution': -4, 'dexterity': 7, 'luck': 3, 'wisdom': 7, 'physical_res': 2, 'magic_res': 2},
        'Necromancer': {'hp': -20, 'strength': -5, 'intelligence': 7, 'constitution': -7, 'dexterity': 3, 'luck': 3, 'wisdom': 7, 'physical_res': -4, 'magic_res': 2},
    }
    
    class_name = character.character_class.name
    stats = class_stats.get(class_name)
    
    if stats:
        for stat, value in stats.items():
            setattr(character, stat, getattr(character, stat) + value)
        character.save()
        
def apply_race_stats(character):
    race_stats = {
        'Human': {'hp': 30, 'strength': 3, 'intelligence': 3, 'constitution': 3, 'dexterity': 3, 'luck': 3, 'wisdom': 3, 'physical_res': 3, 'magic_res': 3},
        'Elf': {'hp': -20, 'strength': -1, 'intelligence': 4, 'constitution': -2, 'dexterity': 4, 'luck': 2, 'wisdom': 4, 'physical_res': -2, 'magic_res': 2},
        'Dwarf': {'hp': 40, 'strength': 6, 'intelligence': -6, 'constitution': 5, 'dexterity': -4, 'luck': -4, 'wisdom': -2, 'physical_res': 7, 'magic_res': 4},
        'Orc': {'hp': 50, 'strength': 7, 'intelligence': -7, 'constitution': 3, 'dexterity': 2, 'luck': -7, 'wisdom': -7, 'physical_res': 4, 'magic_res': -4},
        'Halfling': {'hp': -50, 'strength': 2, 'intelligence': -2, 'constitution': 6, 'dexterity': 6, 'luck': 4, 'wisdom': -2, 'physical_res': 2, 'magic_res': 2},
        'Centaur': {'hp': 20, 'strength': 2, 'intelligence': 2, 'constitution': 2, 'dexterity': 4, 'luck': 4, 'wisdom': 4, 'physical_res': 2, 'magic_res': 2},
        'Half-elf': {'hp': 10, 'strength': 2, 'intelligence': 3, 'constitution': 2, 'dexterity': 4, 'luck': 3, 'wisdom': 3, 'physical_res': 2, 'magic_res': 2},
        'Half-orc': {'hp': 30, 'strength': 6, 'intelligence': -2, 'constitution': -2, 'dexterity': 2, 'luck': 1, 'wisdom': 1, 'physical_res': 1, 'magic_res': 1},
        'Lizardfolk': {'hp': -20, 'strength': 2, 'intelligence': -2, 'constitution': -2, 'dexterity': 6, 'luck': 4, 'wisdom': 2, 'physical_res': 1, 'magic_res': 1},
        'Dragonborn': {'hp': 30, 'strength': 6, 'intelligence': -1, 'constitution': 3, 'dexterity': 3, 'luck': 4, 'wisdom': -1, 'physical_res': -2, 'magic_res': -2},
        'Sylvari': {'hp': -20, 'strength': -3, 'intelligence': 5, 'constitution': 5, 'dexterity': -3, 'luck': 2, 'wisdom': 5, 'physical_res': -2, 'magic_res': -2},
    }
    
    race_name = character.character_race.name
    stats = race_stats.get(race_name)
    
    if stats:
        for stat, value in stats.items():
            setattr(character, stat, getattr(character, stat) + value)
        character.save()
            

def create_character(request):
    existing_character = Character.objects.filter(user=request.user).first()

    if existing_character:
        return redirect('Team:character_list')

    if request.method == 'POST':
        form = CharacterForm(request.POST)

        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            apply_class_stats(character)
            apply_race_stats(character)
            character.save()
            return redirect('Bots_Farm:region_selection')
    else:
        form = CharacterForm()

    return render(request, 'Team/create_character.html', {'form': form})

def level_up(character):
    while character.experience_points >= calculate_experience_for_next_level(character.level):
        character.level += 1
        character.skill_points += 5
        character.save()
        
@login_required
def character_list(request):
    characters = Character.objects.filter(user=request.user)

    if request.method == 'POST':
        character_id = request.POST.get('character_id')
        stat_to_increase = request.POST.get('stat_to_increase')

        # Add support for assigning all skill points to one stat
        if 'assign_all_points' in request.POST:
            character = get_object_or_404(Character, pk=character_id)
            if character.skill_points > 0:
                if stat_to_increase == 'strength':
                    character.strength += character.skill_points
                elif stat_to_increase == 'intelligence':
                    character.intelligence += character.skill_points
                elif stat_to_increase == 'constitution':
                    character.constitution += character.skill_points
                elif stat_to_increase == 'dexterity':
                    character.dexterity += character.skill_points
                elif stat_to_increase == 'wisdom':
                    character.wisdom += character.skill_points
                elif stat_to_increase == 'luck':
                    character.luck += character.skill_points

                character.skill_points = 0
                character.save()
        else:
            character = get_object_or_404(Character, pk=character_id)


            if character.skill_points > 0:
                if stat_to_increase == 'strength':
                    character.strength += 1
                elif stat_to_increase == 'intelligence':
                    character.intelligence += 1
                elif stat_to_increase == 'constitution':
                    character.constitution += 1
                elif stat_to_increase == 'dexterity':
                    character.dexterity += 1
                elif stat_to_increase == 'wisdom':
                    character.wisdom += 1
                elif stat_to_increase == 'luck':
                    character.luck += 1

                character.skill_points -= 1
                character.save()

    for character in characters:
        level_up(character)

        character.life = int(
            character.hp * ((1 + character.constitution * 0.1) * (1 + character.wisdom * 0.1)) / 10)

    experience_needed_for_next_level = None
    if characters:
        experience_needed_for_next_level = calculate_experience_for_next_level(characters[0].level)

    return render(request, 'Team/character_list.html', {'characters': characters, 'experience_needed_for_next_level': experience_needed_for_next_level})