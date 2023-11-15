from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import login


def register(request):
    """Rejestracja nowego użytkownika."""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            user_profile = UserProfile.objects.create(user=new_user)
            login(request, new_user)
            
            return redirect('World:main')

    context = {'form': form}
    return render(request, 'registration/register.html', context)

