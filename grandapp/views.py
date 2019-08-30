from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core import serializers
from .models import Cell
from .models import Drug 
from .models import Tissue
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from .forms import ContactForm
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def cell(request):
    cells = Cell.objects.all()
    return render(request, 'cell.html', {'cells': cells})

#def about(request):
#    form = ContactForm()
#    return render(request, 'about.html', {'contactform':form})

def drug(request):
    drugs = Drug.objects.all()
    return render(request, 'drugs.html', {'drugs': drugs})
    #json  = serializers.serialize('json', drugs)
    #return HttpResponse(json, content_type = 'application/json')

def tissue(request):
    tissues = Tissue.objects.all()
    return render(request, 'tissues.html', {'tissues': tissues})

def about(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_name    = request.POST['contact_name']
            contact_email   = request.POST['contact_email']
            contact_subject = request.POST['contact_subject']
            content         = request.POST['content']
            try:
                send_mail(subject=contact_subject, message=content, from_email=settings.EMAIL_HOST_USER, recipient_list=['marouen.b.guebila@gmail.com',], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
        else:
            return HttpResponse('Error')
    return render(request, "about.html", {'contactform': form})

def thanks(request):
    return HttpResponse('Thank you for your message.')
