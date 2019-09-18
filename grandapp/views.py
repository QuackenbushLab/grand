from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core import serializers
from .models import Cell
from .models import Drug, DrugResultUp, DrugResultDown
from .models import Tissue
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from .forms import ContactForm, GeneForm
from django.conf import settings
import os

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

def analysis(request):
    if request.method == 'GET':
         form = GeneForm()
    else:
         form = GeneForm(request.POST)
         if form.is_valid():
             contentup   = request.POST['contentup']
             contentdown = request.POST['contentdown']
             try:
                 u = open('src/cluereg/data/sampleUp.csv','w')
                 u.write(contentup)
                 u.close()
                 d = open('src/cluereg/data/sampleDown.csv','w')
                 d.write(contentdown)
                 d.close()
                 status = os.system('python3 src/cluereg/lib/enrichCmapReg.py src/cluereg/data/sparse_cmapreg.npz src/cluereg/data/geneNames.csv src/cluereg/data/drugNames.csv src/cluereg/data/sampleUp.csv src/cluereg/data/sampleDown.csv')
                 print(status)
             except BadHeaderError: #find a better exception
                 return HttpResponse('Invalid header found.')
             return redirect('drugresult')
    return render(request, 'analysis.html', {'geneform':form})

def drugresult(request):
    return render(request, 'drugresult.html')

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
            return redirect('erroremail')
    return render(request, "about.html", {'contactform': form})

def thanks(request):
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
    return render(request, "thankyou.html", {'contactform': form})

def erroremail(request):
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
            return redirect('erroremail')
    return render(request, "erroremail.html", {'contactform': form})
