from django.shortcuts import render

def cities(request):
    return render(request, 'Cities/cities.html')
