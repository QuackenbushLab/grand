from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Cell

def home(request):
    cells = Cell.objects.all()
    return render(request, 'home.html', {'cells': cells})

def pet_detail(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except Pet.DoesNotExist:
        raise Http404('Pet not found')
    return render(request, 'pet_detail.html', {'pet': pet})

def about(request):
    return render(request, 'about.html')
