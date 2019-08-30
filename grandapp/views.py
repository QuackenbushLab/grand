from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.core import serializers
from .models import Cell
from .models import Drug 
from .models import Tissue
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.shortcuts import redirect
from .forms import ContactForm
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def cell(request):
    cells = Cell.objects.all()
    return render(request, 'cell.html', {'cells': cells})

#def about(request):
#    return render(request, 'about.html')

def drug(request):
    drugs = Drug.objects.all()
    return render(request, 'drugs.html', {'drugs': drugs})
    #json  = serializers.serialize('json', drugs)
    #return HttpResponse(json, content_type = 'application/json')

def tissue(request):
    tissues = Tissue.objects.all()
    return render(request, 'tissues.html', {'tissues': tissues})

def about(request):
    #check for POST requests on load.
    form = ContactForm()
    request.method == 'POST'
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    email   = request.POST.get('email')

    if subject and message and email:
        try:
            send_mail(subject, message, email, ['benguebila@hsph.harvard.edu'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.') 
        return HttpResponse('Thank your for your email !')

    else:
        #loading contacts.html if no requests
        return render(request, 'about.html')
