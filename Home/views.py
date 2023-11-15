from django.shortcuts import render
from Fight.views import countdown

def home(request):
    """ Main page for app Home """
    return render (request, 'Home/home.html')

def countdown(request):
    return render (request, 'Home/base.html')