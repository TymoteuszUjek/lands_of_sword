from django.shortcuts import render, redirect
from .models import InventoryItem
from Team.models import Character
from django.http import Http404
from django.http import JsonResponse

def inventory(request):
    user = request.user
    inventory_items = InventoryItem.objects.filter(user=user, equipped=True).order_by('-item__level')
    available_items = InventoryItem.objects.filter(user=user, equipped=False).order_by('-item__level')
    
    equipped_item_count = inventory_items.count()
    available_item_count = available_items.count()

    equipped_items_by_type = {}
    inventory_items_by_type = {}

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        try:
            item_to_equip = InventoryItem.objects.get(id=item_id)
        except InventoryItem.DoesNotExist:
            raise Http404("Ten przedmiot nie istnieje.")

        character = Character.objects.get(user=user)
        item_level = item_to_equip.item.level

        if action == 'equip':
            existing_equipped_item = InventoryItem.objects.filter(
                user=user, item_type=item_to_equip.item.item_type, equipped=True).first()

            if character.level >= item_level:
                if existing_equipped_item:
                    existing_equipped_item.equipped = False
                    existing_equipped_item.remove_item_stats() 
                    existing_equipped_item.save()

                item_to_equip.equipped = True
                item_to_equip.apply_item_stats()  
                item_to_equip.save()
            else:
                return JsonResponse({'message': 'Nie masz odpowiedniego poziomu, aby założyć ten przedmiot.'})
        
        elif action == 'unequip':
            item_to_equip.equipped = False
            item_to_equip.remove_item_stats() 
            item_to_equip.save()

    character = Character.objects.get(user=user)
    
    for item in inventory_items:
        if item.item.item_type not in equipped_items_by_type:
            equipped_items_by_type[item.item.item_type] = []
        equipped_items_by_type[item.item.item_type].append(item)

    for item in available_items:
        if item.item.item_type not in inventory_items_by_type:
            inventory_items_by_type[item.item.item_type] = []
        inventory_items_by_type[item.item.item_type].append(item)

    return render(request, 'Inventory/equipment.html', {
        'equipped_items_by_type': equipped_items_by_type,
        'inventory_items_by_type': inventory_items_by_type,
        'equipped_item_count': equipped_item_count,
        'available_item_count': available_item_count,
        'character': character,
    })
