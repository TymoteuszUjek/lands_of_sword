from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Enemy
from Team.models import Character

@login_required
def enemies_list(request):
    enemies = Enemy.objects.all()

    for enemy in enemies:
        enemy.life = int(
            enemy.hp * ((1 + enemy.constitution * 0.1) * (1 + enemy.wisdom * 0.1)) / 10)

    return render(request, 'Bots_Farm/bots_farm.html', {'enemies': enemies})

def region_selection(request):
    user_character = Character.objects.get(user=request.user)
    user_level = user_character.level

    level_ranges = [
        (1, 10),
        (11, 20),
        (21, 30),
        (31, 40),
        (41, 50),
        (51, 60),
        (61, 70),
        (71, 80),
        (81, 100),
    ]

    regions = []

    for min_level, max_level in level_ranges:
        if min_level <= user_level :
            enemies_in_range = Enemy.objects.filter(level__gte=min_level, level__lte=max_level)
            regions.append({
                'min_level': min_level,
                'max_level': max_level,
                'enemies': enemies_in_range,
            })

    return render(request, 'Bots_Farm/region_selection.html', {'regions': regions})
