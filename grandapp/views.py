from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from  .models import Cell
from  .models import Drug 

def home(request):
    return render(request, 'home.html')

def cell(request):
    cells = Cell.objects.all()
    return render(request, 'cell.html', {'cells': cells})

def about(request):
    return render(request, 'about.html')

def drug(request):
    drugs = Drug.objects.all()
    return render(request, 'drugs.html', {'drugs': drugs})
