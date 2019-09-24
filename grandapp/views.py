from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core import serializers
from .models import Cell
from .models import Drug, DrugResultUp, DrugResultDown, Params
from .models import Tissue
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from .forms import ContactForm, GeneForm, DiseaseForm
from django.conf import settings
import os

def home(request):
    return render(request, 'home.html')

def help(request):
    return render(request, 'help.html')

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

def disease(request):
    if request.method == 'GET':
         form = DiseaseForm()
    else:
         form = DiseaseForm(request.POST)
         if form.is_valid():
             content   = request.POST['content']
             try:
                 u = open('src/diseaseEnr/sampleTFGWAS.csv','w')
                 u.write(content)
                 u.close()
                 status  = os.system('python3 src/diseaseEnr/enrichDisease.py src/diseaseEnr/sampleTFGWAS.csv')
                 print(status)
             except BadHeaderError: #find a better exception
                 return HttpResponse('Invalid header found.')
             return redirect('diseaseresult')
    return render(request, 'disease.html', {'diseaseform':form})

def diseaseexample(request):
    if request.method == 'GET':
         form = DiseaseForm({'content':'BHLHE23\nMAX\nMYOD1\nARNTL\nBHLHE40\nMYCN\nCLOCK\nHEY2\nASCL1\nTCF12\nHES6\nFERD3L\nMSGN1\nUSF1\nNEUROD1\nHAND2\nHEY1\nMESP1\nPTF1A\nNPAS2\nNEUROD2\nNHLH1\nATOH1\nARNT2\nOLIG3\nNHLH2\nNEUROG2\nMSC\nHES7\nFOXL1\nTCF3\nVAX1\nBATF\nMAF\nMYC\nDLX2\nIRF4\nIRF8\nKLF4\nCEBPE\n'})
    else:
         form = DiseaseForm(request.POST)
         if form.is_valid():
             content   = request.POST['content']
             try:
                 u = open('src/diseaseEnr/sampleTFGWAS.csv','w')
                 u.write(content)
                 u.close()
                 status  = os.system('python3 src/diseaseEnr/enrichDisease.py src/diseaseEnr/sampleTFGWAS.csv')
                 print(status)
             except BadHeaderError: #find a better exception
                 return HttpResponse('Invalid header found.')
             return redirect('diseaseresult')
    return render(request, 'disease.html', {'diseaseform':form})

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

def analysisexample(request):
    if request.method == 'GET':
         form = GeneForm({'contentup':'ENSG00000137154\nENSG00000160049\nENSG00000281221\nENSG00000137822\nENSG00000113739\nENSG00000139146\nENSG00000099721\nENSG00000147488\nENSG00000116824\nENSG00000013583\nENSG00000105671\nENSG00000012983\nENSG00000013288\nENSG00000102871\nENSG00000226248\nENSG00000102226\nENSG00000136856\nENSG00000108312\nENSG00000132591\nENSG00000175895\nENSG00000198353\nENSG00000130005\nENSG00000177548\nENSG00000110171\nENSG00000026559\nENSG00000170345\nENSG00000173638\nENSG00000125730\nENSG00000198000\nENSG00000125931\nENSG00000176387\nENSG00000232860\nENSG00000229937\nENSG00000197475\nENSG00000135346\nENSG00000213931\nENSG00000030419\nENSG00000156802\nENSG00000146842\nENSG00000196655\nENSG00000110944\nENSG00000228435\nENSG00000156222\nENSG00000146143\nENSG00000177595\nENSG00000019582\nENSG00000160959\nENSG00000185958\nENSG00000256771\nENSG00000139874\nENSG00000116745\nENSG00000140092\nENSG00000120235\nENSG00000128285\nENSG00000156049\nENSG00000157782\nENSG00000168229\nENSG00000111012\nENSG00000170852\nENSG00000147437\nENSG00000088543\nENSG00000108953\nENSG00000125843\nENSG00000170950\nENSG00000148943\nENSG00000124549\nENSG00000196591\nENSG00000169242\nENSG00000175426\nENSG00000105339\nENSG00000163605\nENSG00000132677\nENSG00000134538\nENSG00000158874\nENSG00000085185\nENSG00000135116\nENSG00000168268\nENSG00000102100\nENSG00000172215\nENSG00000165494\nENSG00000198417\nENSG00000102003\nENSG00000169764\nENSG00000057294\nENSG00000167548\nENSG00000183242\nENSG00000116711\nENSG00000100307\nENSG00000103126\nENSG00000137673\nENSG00000116106\nENSG00000111640\nENSG00000174483\nENSG00000073331\nENSG00000110169\nENSG00000250254\nENSG00000163737\nENSG00000204248\nENSG00000198650\nENSG00000125826\n' , 'contentdown':'ENSG00000127528\nENSG00000165487\nENSG00000160181\nENSG00000158815\nENSG00000136932\nENSG00000254997\nENSG00000107104\nENSG00000104881\nENSG00000182326\nENSG00000084093\nENSG00000165792\nENSG00000077498\nENSG00000085788\nENSG00000184302\nENSG00000108861\nENSG00000165280\nENSG00000178445\nENSG00000196372\nENSG00000181143\nENSG00000127125\nENSG00000182446\nENSG00000198056\nENSG00000062485\nENSG00000146276\nENSG00000067064\nENSG00000077380\nENSG00000163946\nENSG00000122299\nENSG00000183549\nENSG00000174483\nENSG00000076382\nENSG00000111716\nENSG00000139718\nENSG00000131747\nENSG00000164035\nENSG00000095319\nENSG00000164081\nENSG00000170075\nENSG00000178053\nENSG00000179477\nENSG00000163624\nENSG00000134243\nENSG00000072682\nENSG00000214022\nENSG00000124783\nENSG00000100941\nENSG00000152402\nENSG00000119655\nENSG00000111450\nENSG00000164128\nENSG00000147804\nENSG00000278548\nENSG00000146834\nENSG00000134684\nENSG00000092345\nENSG00000253293\nENSG00000088726\nENSG00000111328\nENSG00000145244\nENSG00000196646\nENSG00000036549\nENSG00000125726\nENSG00000080709\nENSG00000011295\nENSG00000010256\nENSG00000198815\nENSG00000066044\nENSG00000089154\nENSG00000179455\nENSG00000095752\nENSG00000142657\nENSG00000253729\nENSG00000133740\nENSG00000105229\nENSG00000059145\nENSG00000100342\nENSG00000114742\nENSG00000103187\nENSG00000103174\nENSG00000111145\nENSG00000070366\nENSG00000196954\nENSG00000025156\nENSG00000105997\nENSG00000183648\nENSG00000157150\nENSG00000166167\nENSG00000163754\nENSG00000147457\nENSG00000083896\nENSG00000078142\nENSG00000084112\nENSG00000041357\nENSG00000127948\nENSG00000078403\nENSG00000242372\nENSG00000206073\nENSG00000103994\nENSG00000163739\nENSG00000114867\n' })
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
    params = Params.objects.all()
    return render(request, 'drugresult.html', {'params':params})

def diseaseresult(request):
    params = Params.objects.all()
    return render(request, 'diseaseresult.html', {'params':params})

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
