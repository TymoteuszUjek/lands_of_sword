from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Enemy

@login_required
def regions(request):
    level_ranges = [
        (1, 10),
        (11, 20),
        (21, 30),
    ]

    regions = []

    for min_level, max_level in level_ranges:
        enemies_in_range = Enemy.objects.filter(level__gte=min_level, level__lte=max_level)
        regions.append({
            'min_level': min_level,
            'max_level': max_level,
            'enemies': enemies_in_range,
        })

    return render(request, 'Boss_Fight/regions.html', {'regions': regions})
