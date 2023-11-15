from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from Team.models import Character
from django.db.models import Q

@login_required
def task_master(request):
    user = request.user
    character = Character.objects.get(user=user)

    # Remove completed tasks
    Task.objects.filter(user=user, is_completed=True).delete()

    # Count existing tasks for the user
    existing_tasks_count = Task.objects.filter(user=user).count()

    # Check if the character has an active task
    character.has_active_task = Task.objects.filter(user=user, is_active=True).exists()

    # Calculate how many more tasks can be activated
    remaining_tasks_count = 3 - existing_tasks_count

    # Check and activate tasks based on character level and remaining task count
    tasks_to_activate = []
    if remaining_tasks_count > 0:
        if character.level >= 1:
            tasks_to_activate.append({
                'task_name': f"Defeat {int(10 * (0.5 * character.level))} enemies",
                'task_description': f"Defeat {int(10 * (0.5 * character.level))} enemies in battle.",
                'enemies_to_defeat': int(10 * (0.5 * character.level)),
                'gold_reward': int(50 * character.level)
            })
            remaining_tasks_count -= 1

        if remaining_tasks_count > 0 and character.level >= 1:
            tasks_to_activate.append({
                'task_name': f"Collect {int(100 * character.level)} gold",
                'task_description': f"Collect a total of {int(100 * character.level)} gold from battles or quests.",
                'gold_to_earn': int(100 * character.level),
                'gold_reward': int(100 * character.level)
            })
            remaining_tasks_count -= 1

        if remaining_tasks_count > 0 and character.level >= 1:
            tasks_to_activate.append({
                'task_name': f"Defeat {int(10 * (0.5 * character.level))} players",
                'task_description': f"Defeat {int(10 * (0.5 * character.level))} other players in player vs. player battles.",
                'players_to_defeat': int(10 * (0.5 * character.level)),
                'gold_reward': int(200 * character.level)
            })
            remaining_tasks_count -= 1

        # Activate tasks
        for task_data in tasks_to_activate:
            Task.objects.create(
                user=user,
                task_name=task_data['task_name'],
                task_description=task_data['task_description'],
                enemies_to_defeat=task_data.get('enemies_to_defeat', 0),
                gold_to_earn=task_data.get('gold_to_earn', 0),
                players_to_defeat=task_data.get('players_to_defeat', 0),
                gold_reward=task_data['gold_reward'],
                is_completed=False,
                is_active=False
            )

    # Retrieve tasks for the user
    tasks = Task.objects.filter(user=user)

    return render(request, 'Tavern/task_master.html', {'tasks': tasks, 'character': character})


@login_required
def activate_task(request, task_id):
    user = request.user
    existing_active_task = Task.objects.filter(user=user, is_active=True).first()

    if existing_active_task:
        # Redirect if there's already an active task
        return redirect('Tavern:task_master')

    task = Task.objects.get(pk=task_id)
    character = Character.objects.get(user=user)

    # Set character's progress for the new task
    character.killed_monsters = 0
    character.collected_gold = 0
    character.killed_players = 0
    character.save()

    # Activate the selected task
    task.is_active = True
    task.save()
    return redirect('Tavern:task_master')


@login_required
def complete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    character = Character.objects.get(user=request.user)

    # Check if there's an active task; if yes, redirect back
    #if Task.objects.filter(user=request.user, is_active=True).exists():
        #return redirect('Tavern:task_master')

    if task.is_active and not task.is_completed:
        if task.enemies_to_defeat > 0 and character.killed_monsters < task.enemies_to_defeat:
            return redirect('Tavern:task_master')

        elif task.gold_to_earn > 0 and character.collected_gold < task.gold_to_earn:
            return redirect('Tavern:task_master')

        elif task.players_to_defeat > 0 and character.killed_players < task.players_to_defeat:
            return redirect('Tavern:task_master')

        # Player has met the task requirements, grant reward and mark task as completed
        character.gold += int(task.gold_reward)
        character.save()

        task.is_completed = True
        task.is_active = False
        task.save()

    return redirect('Tavern:task_master')

@login_required
def claim_reward(request, task_id):
    task = Task.objects.get(pk=task_id)
    character = Character.objects.get(user=request.user)

    if task.is_completed:
        if task.gold_reward > 0:
            character.gold += int(task.gold_reward)
            character.save()

        # Reset task progress
        character.killed_monsters = 0
        character.collected_gold = 0
        character.killed_players = 0
        character.save()

        # Reset task
        task.is_completed = False
        task.save()

    return redirect('Tavern:task_master')

@login_required
def reset_tasks(request):
    user = request.user

    # Delete all user tasks
    Task.objects.filter(user=user).delete()


    return redirect('Tavern:task_master')