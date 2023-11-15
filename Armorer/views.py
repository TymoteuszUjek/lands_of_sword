from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction
from Items.models import Item
from Team.models import Character
from Inventory.models import InventoryItem
from django.utils import timezone
import math
from django.urls import reverse

@login_required
def armorer(request):
    try:
        character = Character.objects.get(user=request.user)
    except Character.DoesNotExist:
        return redirect('Team:create_character')

    user_gold = character.gold
    user_inventory = InventoryItem.objects.filter(user=request.user, equipped=False)


    items_for_sale = Item.objects.filter(shop_type=' Armorer').exclude(
        inventoryitem__user=request.user, inventoryitem__equipped=False)[:10]
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        item = Item.objects.get(pk=item_id)

        if action == 'buy':
            if item.price <= user_gold:
                character.gold -= item.price
                character.save()
                inventory_item = InventoryItem(user=request.user, item=item)
                inventory_item.item_type += item.item_type
                inventory_item.shop_type += item.shop_type
                inventory_item.name += item.name
                inventory_item.level += item.level
                inventory_item.hp += item.hp
                inventory_item.damage += item.damage
                inventory_item.strength += item.strength
                inventory_item.intelligence += item.intelligence
                inventory_item.constitution += item.constitution
                inventory_item.dexterity += item.dexterity
                inventory_item.luck += item.luck
                inventory_item.wisdom += item.wisdom
                inventory_item.rarity += item.rarity
                inventory_item.price += item.price
                inventory_item.physical_res += item.physical_res
                inventory_item.magic_res += item.magic_res
                inventory_item.enhancement_level += item.enhancement_level
                inventory_item.enhancement_cost += item.enhancement_cost
                inventory_item.save()
                messages.success(request, f"You bought {inventory_item.name}.")
            else:
                messages.error(request, "Insufficient gold to buy this item.")

            # Get the current time after the action has been performed
            current_time = timezone.now()

            # Update counter only if purchased
            transaction = Transaction(user=request.user, item=item, transaction_type='buy', price=item.price, transaction_date=current_time)
            transaction.save()
            
            return HttpResponseRedirect(reverse('Armorer:armorer'))

        elif action == 'sell':
            # Handle the case where multiple items could be returned
            inventory_items = InventoryItem.objects.filter(user=request.user, item=item, equipped=False)

            if inventory_items.exists():
                # If there are multiple items, delete the first one and log a message
                inventory_item = inventory_items.first()
                character.gold += item.price
                inventory_item.enhancement_level = 0
                inventory_item.enhancement_cost = item.base_enhancement_cost
                inventory_item.damage = item.base_damage
                inventory_item.strength = item.base_strength
                inventory_item.intelligence = item.base_intelligence 
                inventory_item.constitution = item.base_constitution
                inventory_item.dexterity = item.base_dexterity
                inventory_item.luck = item.base_luck
                inventory_item.wisdom = item.base_wisdom
                inventory_item.price = item.base_price
                inventory_item.physical_res = item.base_physical_res
                inventory_item.magic_res = item.base_magic_res
                inventory_item.hp = item.base_hp
                inventory_item.save()
                item.save()
                character.save()
                inventory_item.delete()
                messages.success(request, f"You sold {item.name}.")
                
                
            return HttpResponseRedirect(reverse('Armorer:armorer'))
        
        elif action == 'upgrade':
            try:
                inventory_item = InventoryItem.objects.get(user=request.user, item=item)
            except InventoryItem.DoesNotExist:
                messages.error(request, "Item not found in your inventory.")
                return HttpResponseRedirect(reverse('Armorer:armorer'))

            if character.gold >= inventory_item.enhancement_cost and inventory_item.enhancement_level < 20:
                character.gold -= inventory_item.enhancement_cost
                inventory_item.apply_upgraded_stats()
                inventory_item.save()
                character.save()
                messages.success(request, f"You successfully upgraded {inventory_item.name} to level {inventory_item.enhancement_level}.")
            else:
                messages.error(request, "Insufficient gold to upgrade this item.")

            return HttpResponseRedirect(reverse('Armorer:armorer'))


    # Calculate your remaining purchases
    remaining_purchases = max(0, 10 - Transaction.objects.filter(user=request.user, transaction_type='buy', transaction_date__gte=timezone.now() - timezone.timedelta(minutes=3)).count())

    # Calculate remaining time in seconds
    last_transaction_time = Transaction.objects.filter(
        user=request.user,
        transaction_type='buy',
        transaction_date__gte=timezone.now() - timezone.timedelta(minutes=3)
    ).last()

    if last_transaction_time:
        elapsed_time = timezone.now() - last_transaction_time.transaction_date
        remaining_time_seconds = max(0, 180 - math.ceil(elapsed_time.total_seconds()))
    else:
        remaining_time_seconds = 0

    remaining_time_minutes = remaining_time_seconds // 60
    remaining_time_seconds %= 60

    context = {
        'items_for_sale': items_for_sale,
        'user_gold': user_gold,
        'user_inventory': user_inventory,
        'remaining_purchases': remaining_purchases,
        'remaining_time_minutes': remaining_time_minutes,
        'remaining_time_seconds': remaining_time_seconds
    }

    return render(request, 'Armorer/armorer.html', context)