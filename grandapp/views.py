from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core import serializers
from .models import Cell, Disease, Cancer
from .models import Druglanding, DrugResultUp, DrugResultDown, Params, Tcgasample, Geosample, Genelanding
from .models import Tissue, Gwas, TissueEx, TissueTar, Tissuelanding, Tissuesample, Cancerlanding, Drugsample
from .models import Drugdesc, Breastsample, Cervixsample, Liversample, Ggbmd1sample, Ggbmd2sample, Ggnsample
from .models import Pancreassample
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from .forms import ContactForm, GeneForm, DiseaseForm, NetForm
from django.conf import settings
import os
import random
import time
from django.core import serializers

# for enrich disease
import pandas as pd
import scipy.stats as stats
import numpy as  np
import requests
from statsmodels.stats import multitest # for fdr correction

# to fetch single-sample network
from io import StringIO # python3; python2: BytesIO 
import boto3

# for enrich drug
import scipy as sp # for sparse matrices
import scipy.sparse
import sys # for arguments
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import inv

def home(request):
    params  = Params.objects.filter(id=-1)
    print(params)
    return render(request, 'home.html', {'params':params})

def help(request):
    return render(request, 'help.html')

def download(request):
    return render(request, 'download.html')

def cell(request):
    cells = Cell.objects.all()
    return render(request, 'cell.html', {'cells': cells})

def genes(request):
    geneslanding = Genelanding.objects.all()
    return render(request, 'genes.html',{'geneslanding':geneslanding})

def networksagg(request,slug):
    if request.method == 'GET':
        form = NetForm({'dt':'no','topbottom':'Largest','nedges':100})
        nodes = pd.DataFrame(data=['TF','Gene'])
        nodes['id']=[0,1]
        nodes.columns = ['label','id']
        nodes['shape']= ['triangle'] + ['circle']
        nodes['color']=['#98c4e1']   + ['#d7cad1']
        edges= pd.DataFrame(data=[0.5])
        edges.columns=['value']
        edges['from']=0
        edges['to']  =1
        edges['arrows']='to'
        nodes=nodes.to_json(orient='records')
        edges=edges.to_json(orient='records')
    else:
        form = NetForm(request.POST)
        if form.is_valid():
            seconds = time.time()
            fetchNet='local'
            nedges    = int(request.POST['nedges'])
            topbottom = request.POST['topbottom']
            dt         = request.POST.get('dt', False)
            brd        = request.POST.get('brd', False)
            print('The number of edges is',nedges)
            print(brd)
            if fetchNet=='server':
                client = boto3.client('s3')
                bucket_name = 'granddb'
                object_key = 'cancer/colon_cancer/networks/panda/Colon_cancer_TCGA.csv'
                csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
                body = csv_obj['Body']
                csv_string = body.read().decode('utf-8')
                df = pd.read_csv(StringIO(csv_string),index_col=0,sep=',')
            elif fetchNet=='local':
                df = pd.read_csv('/Users/mab8354/Colon_cancer_TCGA.csv',index_col=0,sep=',')
            if dt=='dtt':
                tftar  = df.sum(axis=1) 
                genetar= df.sum(axis=0)
            if dt=='dee':
                deDf = pd.read_csv('/Users/mab8354/cancer_colon_expression_tcga.txt',index_col=0,sep='\t')
                deDfmean = deDf.values.mean()
                deDf = deDf.mean(axis=1)
            df=df.stack().reset_index().rename(columns={'TF':'source','level_1':'target', 0:'value'})
            df=df.sort_values(by=['value'])
            if topbottom=='Smallest':
                df=df.iloc[0:nedges,]
            elif topbottom=='Largest':
                df=df.iloc[(len(df)-nedges):len(df),]
            b1, c1 = np.unique(df.source, return_inverse=True)    
            b2, c2 = np.unique(df.target, return_inverse=True)  
            nodes = pd.DataFrame(data=np.concatenate((b1,b2)))
            nodes['id']=list(range(0,len(b1)+len(b2)))
            nodes.columns  = ['label','id']
            nodes['shape'] = ['triangle']*len(b1) + ['circle']*len(b2)
            nodes['color'] = ['#98c4e1']*len(b1) + ['#d7cad1']*len(b2)
            if dt=='dee':
                nodes['value'] = deDfmean
                bb1  = np.intersect1d(b1,deDf.index)
                bb2  = np.intersect1d(b2,deDf.index)
                indInter = np.in1d(nodes.label, np.concatenate((bb1,bb2)))
                nodes['value'][indInter] = np.concatenate((deDf[bb1],deDf[bb2]))
                bb1,bb2,deDf=[],[],[]
            if dt=='dtt':
                nodes['value'] = np.concatenate((tftar[b1],genetar[b2]))
            edges          = df
            edges['from']  = c1
            edges['to']    = np.max(c1)+1+c2
            edges['color'] = 'green'
            edges['color'][df.value < 0] = 'red'
            print(brd)
            if brd==False:
                del edges['value']
            elif brd=='on':
                edges.value   = np.abs(edges.value)
            edges['arrows']= 'to'
            del edges['source'] 
            del edges['target']
            df=''
            nodes=nodes.to_json(orient='records')
            edges=edges.to_json(orient='records')
            seconds2 = time.time()
            print(seconds2-seconds)
    cancerType=slug[:(len(slug)-8)].capitalize()
    if int(slug[len(slug)-1])==1:
        dataset='TCGA'
    elif int(slug[len(slug)-1])==2:
        dataset='GEO'
    outputDict = {'cancerType': cancerType, 'dataset':dataset, 'netform':form, 'nodes':nodes, 'edges':edges}
    return render(request, 'networksagg.html', outputDict)

def drug(request):
    return render(request, 'drugs.html')

def druglanding(request):
    drugslanding = Druglanding.objects.all()
    drugsample   = Drugsample.objects.all()
    query=request.path_info[7:-6]
    drugdesc     = Drugdesc.objects.get(pert_iname=query)
    if "/" in query:
        query2=query.replace("/", "")
        drugdesc.image_name=query2
    else:
        drugdesc.image_name=query
    drugdesc.save()
    drugslanding = drugslanding.filter(drug=query)
    drugsample   = drugsample.filter(pert_iname=query)
    return render(request, 'drugslanding.html', {'drugslanding': drugslanding,'drugsample':drugsample,'drugdesc':drugdesc})

def disease(request):
    if request.method == 'GET':
         form = DiseaseForm()
    else:
         form = DiseaseForm(request.POST)
         if form.is_valid():
             content   = request.POST['content']
             data = content.split('\r\n')
             data = list(filter(None, data))
             contentdf = pd.DataFrame(data, columns = ['Gene'])
             try:
                 #u = open('src/diseaseEnr/sampleTFGWAS.csv','w')
                 #u.write(content)
                 #u.close()
                 qval, pvalVec, tfdb, nCondVec, qval1, pvalVec1, tfdb1, nCondVec1,stat1,stat2,qvalTE,pvalVecTE,nCondVecTE,qvalTT,pvalVecTT,nCondVecTT,tfdbTE,tfdbTT=enrichDisease(contentdf)
                 randid = random.randint(1,1000000)
                 indSortP  = np.argsort(pvalVec)
                 pvalVec   = pvalVec[indSortP]
                 qval      = qval[indSortP]
                 nCondVec  = nCondVec[indSortP]
                 tfdb      = tfdb.iloc[indSortP]
                 max_display=100
                 counter = Params.objects.get(id=-1)
                 newID   = counter.genesupin % 10
                 for i in range(max_display):
                     disease = Disease.objects.get(idd=i+1, nuser=newID)
                     disease.disease  =tfdb.iloc[i,0]
                     disease.count    =tfdb.iloc[i,3]
                     disease.intersect=nCondVec[i]
                     disease.pval     =round(pvalVec[i],5)
                     disease.qval     =round(qval[i],5)
                     disease.hpoId    ='https://hpo.jax.org/app/browse/term/' + tfdb.iloc[i,5]
                     disease.query    =randid
                     disease.save()
                 for i in range(len(qval1)):
                     gwas   = Gwas.objects.get(idd=i+1, nuser=newID)
                     gwas.disease     =tfdb1.iloc[i,0]
                     gwas.count       =tfdb1.iloc[i,3]
                     gwas.intersect   =nCondVec1[i]
                     gwas.pval        =round(pvalVec1[i],5)
                     gwas.qval        =round(qval1[i],5)
                     gwas.query       =randid
                     gwas.save()
                 for i in range(len(qvalTE)):
                     tissueex   = TissueEx.objects.get(idd=i+1, nuser=newID)
                     tissueex.tissue      =tfdbTE['Tissues'].iloc[i]
                     tissueex.count       =tfdbTE['Cond'].iloc[i]
                     tissueex.intersect   =nCondVecTE[i]
                     tissueex.pval        =round(pvalVecTE[i],5)
                     tissueex.qval        =round(qvalTE[i],5)
                     tissueex.tissueLink  ='https://grand.networkmedicine.org/tissues/' + tissueex.tissue + '_tissue/'
                     tissueex.query       =randid
                     tissueex.save()
                 for i in range(len(qvalTT)):
                     tissuett   = TissueTar.objects.get(idd=i+1, nuser=newID)
                     tissuett.tissue      =tfdbTT['Tissue'].iloc[i]
                     tissuett.count       =tfdbTT['#TFsDifferentiallyTargetingSelectedCategories'].iloc[i]
                     tissuett.intersect   =nCondVecTT[i]
                     tissuett.pval        =round(pvalVecTT[i],5)
                     tissuett.qval        =round(qvalTT[i],5)
                     tissuett.tissueLink  ='https://grand.networkmedicine.org/tissues/' + tissuett.tissue + '_tissue/'
                     tissuett.query       =randid
                     tissuett.save()
                 accessKey = randid
                 param=Params.objects.get(id=newID)
                 param.genesdownin   =stat1
                 param.genesupin     =stat2
                 param.query         =randid
                 param.save()  
                 counter=Params.objects.get(id=-1)
                 counter.genesupin+=1
                 counter.save()
             except BadHeaderError: #find a better exception
                 return HttpResponse('Invalid header found.')
             return redirect('/diseaseresult/'+str(accessKey)+'/gwas/')
    return render(request, 'disease.html', {'diseaseform':form})

def diseaseexample(request):
    if request.method == 'GET':
         form = DiseaseForm({'content':'BHLHE23\nMAX\nMYOD1\nARNTL\nBHLHE40\nMYCN\nCLOCK\nHEY2\nASCL1\nTCF12\nHES6\nFERD3L\nMSGN1\nUSF1\nNEUROD1\nHAND2\nHEY1\nMESP1\nPTF1A\nNPAS2\nNEUROD2\nNHLH1\nATOH1\nARNT2\nOLIG3\nNHLH2\nNEUROG2\nMSC\nHES7\nFOXL1\nTCF3\nVAX1\nBATF\nMAF\nMYC\nDLX2\nIRF4\nIRF8\nKLF4\nCEBPE\n'})
    else:
         form = DiseaseForm(request.POST)
         if form.is_valid():
             content   = request.POST['content']
             data=content.split('\r\n')
             data = list(filter(None, data))
             contentdf = pd.DataFrame(data, columns = ['Gene'])
             try:
                 #u = open('src/diseaseEnr/sampleTFGWAS.csv','w')
                 #u.write(content)
                 #u.close()
                 qval, pvalVec, tfdb, nCondVec, qval1, pvalVec1, tfdb1, nCondVec1,stat1,stat2=enrichDisease(contentdf)
                 indSortP  = np.argsort(pvalVec)
                 pvalVec   = pvalVec[indSortP]
                 qval      = qval[indSortP]
                 nCondVec  = nCondVec[indSortP]
                 tfdb      = tfdb.iloc[indSortP]
                 max_display=100
                 for i in range(max_display):
                     disease = Disease.objects.get(id=i+1)
                     disease.disease  =tfdb.iloc[i,0]
                     disease.count    =tfdb.iloc[i,3]
                     disease.intersect=nCondVec[i]
                     disease.pval     =round(pvalVec[i],5)
                     disease.qval     =round(qval[i],5)
                     disease.query    =disease.query+1
                     disease.save()
                 for i in range(len(qval1)):
                     gwas   = Gwas.objects.get(id=i+1)
                     gwas.disease     =tfdb1.iloc[i,0]
                     gwas.count       =tfdb1.iloc[i,3]
                     gwas.intersect   =nCondVec1[i]
                     gwas.pval        =round(pvalVec1[i],5)
                     gwas.qval        =round(qval1[i],5)
                     gwas.save()
                 accessKey = disease.query
                 counter= Params.objects.get(id=0)
                 newID  = counter.genesupin % 10
                 param=Params.objects.get(id=newID+1)
                 param.genesdownin   =stat1
                 param.genesupin     =stat2
                 param.save()
             except BadHeaderError: #find a better exception
                 return HttpResponse('Invalid header found.')
             return redirect('/diseaseresult/'+str(accessKey)+'/')
    return render(request, 'disease.html', {'diseaseform':form})

def tissue(request):
    tissues = Tissue.objects.all()
    return render(request, 'tissues.html', {'tissues': tissues})

def tissuelanding(request,slug):
    tissuelanding = Tissuelanding.objects.filter(tissue=slug.replace('_',' ')[:-7])
    tissuesample = Tissuesample.objects.filter(grdid=slug) 
    name= 'yes'
    if slug in ['Lymphoblastoid_cell_line_tissue','Fibroblast_cell_line_tissue','Kidney_cortex_tissue','Minor_salivary_gland_tissue',
               'Ovary_tissue','Prostate_tissue','Testis_tissue','Uterus_tissue','Vagina_tissue']:
        name='no'
    return render(request, "tissueslanding.html", {'tissuelanding': tissuelanding, 'slug':slug,'tissuesample':tissuesample, 'name':name})

def cancer(request):
    cancer = Cancer.objects.all()
    return render(request, 'cancer.html', {'cancer': cancer})

def cancerlanding(request,slug):
    cancerlanding = Cancerlanding.objects.filter(cancer=slug.replace('_',' '))
    geo,tool,tcgasample='no','otter',''
    #initialize data variables
    nsamples,ndata,nagg=0,0,0
    if slug == 'Cervix_cancer':
        tcgasample = Cervixsample.objects.all()
        nsamples,ndata,nagg=0,1,1
    elif slug == 'Breast_cancer':
        tcgasample = Breastsample.objects.all()
        nsamples,ndata,nagg=0,1,1
    elif slug == 'Liver_cancer':
        tcgasample = Liversample.objects.all()
        nsamples,ndata,nagg=0,1,1
    returntupl = {'cancerlanding': cancerlanding, 'slug':slug[0:(len(slug)-7)], 'geo':geo, 'tool':tool, 
                  'tcgasample':tcgasample, 'nsamples':nsamples,'ndata':ndata, 'nagg':nagg}
    if slug == 'Colon_cancer':
        tcgasample   = Tcgasample.objects.all()
        geosample    = Geosample.objects.all()
        geo,tool='yes','panda'
        nsamples,ndata,nagg=1638,2,2
        returntupl   = {'cancerlanding': cancerlanding, 'slug':slug[0:(len(slug)-7)], 'tcgasample':tcgasample,
                        'geosample':geosample,'geo':geo,'tool':tool, 'nsamples':nsamples,'ndata':ndata, 'nagg':nagg}
    if slug == 'Glioblastoma_cancer':
        ggbmd1sample   = Ggbmd1sample.objects.all()
        ggbmd2sample   = Ggbmd2sample.objects.all()
        ggnsample      = Ggnsample.objects.all()
        geo,tool='yes','panda'
        nsamples,ndata,nagg=1023,3,3
        returntupl   = {'cancerlanding': cancerlanding, 'slug':slug[0:(len(slug)-7)], 'ggbmd1sample':ggbmd1sample,
                        'geosample':ggnsample,'geo':geo,'tool':tool, 'nsamples':nsamples,'ndata':ndata, 'nagg':nagg, 
                        'ggbmd2sample':ggbmd2sample,}
    if slug == 'Pancreas_cancer':
        pancreassample   = Pancreassample.objects.all()
        geo,tool='no','panda'
        nsamples,ndata,nagg=150,1,0
        returntupl   = {'cancerlanding': cancerlanding, 'slug':slug[0:(len(slug)-7)], 'tcgasample':pancreassample,
                        'geo':geo,'tool':tool, 'nsamples':nsamples,'ndata':ndata, 'nagg':nagg}
    return render(request, "cancerlanding.html", returntupl)

def analysis(request):
    if request.method == 'GET':
         form = GeneForm({'tfgene':''}, auto_id=True)
    else:
         form = GeneForm(request.POST)
         if form.is_valid():
             contentup   = request.POST['contentup']
             contentdown = request.POST['contentdown']
             tfgene      = request.POST['tfgene']
             brd         = request.POST.get('brd', False)
             max_display = int(request.POST['ngenes'])
             data=contentup.split('\r\n')
             data = list(filter(None, data))
             sampleUp = pd.DataFrame(data, columns = ['Gene'])
             data=contentdown.split('\r\n')
             data = list(filter(None, data))
             sampleDown = pd.DataFrame(data, columns = ['Gene'])
             try:
                 if tfgene=='Gene targeting':
                     gene=1
                 elif tfgene=='TF targeting':
                     gene=0
                 drugNames, cosDist, overlap, indSort, stat1, stat2, stat3, stat4, drugDF = enrichCmapReg(gene,sampleUp,sampleDown,brd)
                 #max_display=100
                 randid      =random.randint(1,1000000)
                 counter= Params.objects.get(id=-1)
                 newID  = counter.genesupin % 10
                 i=0
                 for i in range(max_display):
                     drug=DrugResultUp.objects.get(idd=i+1, nuser=newID)
                     currDrugName = drugNames[indSort[i]]
                     drug.orig    = currDrugName
                     drug.drug    = currDrugName[0].upper() + currDrugName[1:]
                     drug.cosine  = round(cosDist[indSort[i]],4)
                     drug.overlap = overlap[indSort[i]]
                     drug.druglink= 'https://grand.networkmedicine.org/drugs/' + drug.drug + '-drug/'
                     drug.query   = randid
                     drug.altid           =drugDF.iloc[indSort[i],1]
                     drug.inchi_key_prefix=drugDF.iloc[indSort[i],5]
                     drug.inchi_key       =drugDF.iloc[indSort[i],6]
                     drug.canonical_smiles=drugDF.iloc[indSort[i],7]
                     drug.pubchem_cid     =drugDF.iloc[indSort[i],8]
                     drug.save()
                     drug=DrugResultDown.objects.get(idd=i+1, nuser=newID)
                     currDrugName = drugNames[indSort[-1-i]]
                     drug.orig    = currDrugName
                     drug.drug    = currDrugName[0].upper() + currDrugName[1:]
                     drug.cosine  = round(cosDist[indSort[-1-i]],4)
                     drug.overlap = overlap[indSort[-1-i]]
                     drug.druglink= 'https://grand.networkmedicine.org/drugs/' + drug.drug + '-drug/'
                     drug.query   = randid
                     drug.altid           =drugDF.iloc[indSort[-1-i],1]
                     drug.inchi_key_prefix=drugDF.iloc[indSort[-1-i],5]
                     drug.inchi_key       =drugDF.iloc[indSort[-1-i],6]
                     drug.canonical_smiles=drugDF.iloc[indSort[-1-i],7]
                     drug.pubchem_cid     =drugDF.iloc[indSort[-1-i],8]
                     drug.save()
                     i+=1
                     #payload = {'drug':drugNames.iloc[indSort[-1-i]],'cosine':round(cosDist[indSort[-1-i]],4),'overlap':overlap[indSort[-1-i]]}
                 accessKey = randid
                 param  = Params.objects.get(id=newID)
                 param.genesupin   = stat1
                 param.genesdownin = stat2
                 param.genesup     = stat3
                 param.genesdown   = stat4
                 param.query       = randid
                 param.save()
                 counter=Params.objects.get(id=-1)
                 counter.genesupin+=1
                 counter.save()
             except BadHeaderError: #find a better exception
                 return HttpResponse('Invalid header found.')
             return redirect('/drugresult/' + str(accessKey) + '/reverse/')
    return render(request, 'analysis.html', {'geneform':form})

def drugresult(request, id):
    params   = Params.objects.filter(query=id)
    drugdown = DrugResultDown.objects.filter(query=id)
    data = serializers.serialize("json", drugdown)
    sense='reverse'
    return render(request, 'drugresult.html', {'params':params,'drugdown':drugdown,'id':id, 'data': data, 'sense':sense})

def drugresultsimilar(request, id):
    params = Params.objects.filter(query=id)
    drugup = DrugResultUp.objects.filter(query=id)
    data = serializers.serialize("json", drugup)
    sense='similar'
    return render(request, 'drugresultsimilar.html', {'params':params,'drugup':drugup,'id':id, 'data': data, 'sense':sense})

def diseasegwas(request, id):
    params  = Params.objects.filter(query=id)
    gwas    = Gwas.objects.filter(disease='Response to anti-retroviral therapy ddI d4T in HIV-1 infection grade 3 peripheral neuropathy')
    for objectgwas in gwas:
        objectgwas.disease ='Response to anti-retroviral therapy'
        objectgwas.save()
    gwas    = Gwas.objects.filter(disease='Primary tooth development time to first tooth eruption')
    for objectgwas in gwas:
        objectgwas.disease ='Primary tooth to first tooth eruption'
        objectgwas.save()
    gwas    = Gwas.objects.filter(query=id)
    for objectgwas in gwas:
        objectgwas.logpval = -np.log10(objectgwas.pval )
        objectgwas.save()
    gwas    = Gwas.objects.filter(query=id)
    data = serializers.serialize("json", gwas)
    sense='gwas'
    return render(request, 'diseaseresultgwas.html', {'params':params,'gwas':gwas,'id':id, 'data': data, 'sense':sense})

def diseasehpo(request, id):
    params  = Params.objects.filter(query=id)
    disease = Disease.objects.filter(query=id)
    sense='disease'
    for objectdisease in disease:
        objectdisease.logpval = -np.log10(objectdisease.pval )
        objectdisease.save()
        disease = Disease.objects.filter(query=id)
    data = serializers.serialize("json", disease)
    return render(request, 'diseaseresulthpo.html', {'params':params,'disease':disease,'id':id, 'data': data, 'sense':sense})

def diseasetissueex(request, id):
    params  = Params.objects.filter(query=id)
    tissueex   = TissueEx.objects.filter(query=id)
    sense='tissueex'
    tissueex   = TissueEx.objects.filter(query=id)
    for objecttissuex in tissueex:
        objecttissuex.logpval = -np.log10(objecttissuex.pval)
        if np.isinf(objecttissuex.logpval):
            objecttissuex.logpval = 10
        objecttissuex.save()
    data = serializers.serialize("json", tissueex)
    return render(request, 'diseaseresulttissueex.html', {'params':params,'tissueex':tissueex,'id':id, 'data': data, 'sense':sense})

def diseasetissuetar(request, id):
    params     = Params.objects.filter(query=id)
    tissuetar  = TissueTar.objects.filter(query=id)
    sense='tissuetar'
    tissuetar  = TissueTar.objects.filter(query=id)
    for objecttissutar in tissuetar:
        objecttissutar.logpval = -np.log10(objecttissutar.pval)
        if np.isinf(objecttissutar.logpval):
            objecttissutar.logpval = 10
        objecttissutar.save()
    data = serializers.serialize("json", tissuetar)
    return render(request, 'diseaseresulttissuetar.html', {'params':params,'tissuetar':tissuetar,'id':id, 'data': data, 'sense':sense})

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

def enrichDisease(tflist):
    #Read query
    #tflist = pd.read_csv('src/diseaseEnr/sampleTFGWAS.csv',header=None)

    #Read all TF names
    alltfs = pd.read_csv('src/diseaseEnr/TF_names_v_1.01.csv', header=None)

    # 1. GWAS
    #Read TF db
    tfdbgwas = pd.read_csv('src/diseaseEnr/TF-disease-data_Fig4_GWAS.csv')
    tfdbgwas = tfdbgwas.iloc[:170,:]

    #Compute p-values
    pvalVec = np.zeros(len(tfdbgwas))
    nCondVec= np.zeros(len(tfdbgwas))
    totPop  = 1639 #total number in population according to Lambert et al, Cell, 2018.
    #totCond = np.zeros()#total number with condition in population
    nSubset = len(tflist)#size of subset
    #nCond   = #n condition in subset
    for i in range(len(tfdbgwas)):
        totCond       = tfdbgwas.iloc[i,3]
        gt            = tfdbgwas.iloc[i, 4].split(',')[:-2]
        nCond         = len(set(gt).intersection(set(tflist.iloc[:, 0])))
        nCondVec[i]   = nCond
        pvalVec[i]    = stats.hypergeom.sf(nCond - 1,totPop,totCond,nSubset)

    qval = multitest.fdrcorrection(pvalVec)
    qval = qval[1]
    # for i in range(len(tfdbgwas)):
    #     payload = {'disease':tfdbgwas.iloc[i,0] ,'count':tfdbgwas.iloc[i,3],'intersect':nCondVec[i],'pval':round(pvalVec[i],5),'qval':round(qval[i],5)}
    #     r = requests.put('http://localhost:8000/api/v1/gwas/' + str(i+1) + '/', data=payload)
    qval1    = qval
    nCondVec1= nCondVec
    pvalVec1 = pvalVec

    #2. Disease
    tfdbdisease = pd.read_csv('src/diseaseEnr/TF-disease-data_Fig4_disease.csv')

    #Compute p-values
    pvalVec = np.zeros(len(tfdbdisease))
    nCondVec= np.zeros(len(tfdbdisease))
    totPop  = 1639 #total number in population according to Lambert et al, Cell, 2018.
    #totCond = np.zeros()#total number with condition in population
    nSubset = len(tflist) #size of subset
    #nCond   = #n condition in subset
    for i in range(len(tfdbdisease)):
        totCond       = tfdbdisease.iloc[i,3]
        gt            = tfdbdisease.iloc[i, 4].split(',')[:-2]
        nCond         = len(set(gt).intersection(set(tflist.iloc[:, 0])))
        nCondVec[i]   = nCond
        pvalVec[i]    = stats.hypergeom.sf(nCond - 1,totPop,totCond,nSubset)

    qval = multitest.fdrcorrection(pvalVec)
    qval = qval[1]

    #3. Tissue Expression
    tftissueex = pd.read_csv('src/diseaseEnr/TF-tissue-expression.csv')

    #Compute p-values
    pvalVecTE = np.zeros(len(tftissueex))
    nCondVecTE= np.zeros(len(tftissueex))
    totPop  = 1639
    nSubset = len(tflist) #size of subset
    #nCond   = #n condition in subset
    for i in range(len(tftissueex)):
        totCond       = tftissueex['Cond'].iloc[i]
        gt            = tftissueex['TFs'].iloc[i].split(',')[:-2]
        nCond         = len(set(gt).intersection(set(tflist.iloc[:, 0])))
        nCondVecTE[i]   = nCond
        pvalVecTE[i]    = stats.hypergeom.sf(nCond - 1,totPop,totCond,nSubset)

    qvalTE = multitest.fdrcorrection(pvalVecTE)
    qvalTE = qvalTE[1]

    #4. Tissue Expression
    tftissuetar = pd.read_csv('src/diseaseEnr/TF-tissue-target.csv')

    #Compute p-values
    pvalVecTT = np.zeros(len(tftissuetar))
    nCondVecTT= np.zeros(len(tftissuetar))
    totPop  = 1639
    nSubset = len(tflist) #size of subset
    #nCond   = #n condition in subset
    for i in range(len(tftissuetar)):
        totCond       = tftissuetar['#TFsDifferentiallyTargetingSelectedCategories'].iloc[i]
        gt            = tftissuetar['DifferentiallyTargetingTFs'].iloc[i].split(',')
        nCond         = len(set(gt).intersection(set(tflist.iloc[:, 0])))
        nCondVecTT[i]   = nCond
        pvalVecTT[i]    = stats.hypergeom.sf(nCond - 1,totPop,totCond,nSubset)

    qvalTT = multitest.fdrcorrection(pvalVecTT)
    qvalTT = qvalTT[1]

    stat1=len(set(alltfs.iloc[:,0]).intersection(set(tflist.iloc[:,0])))
    stat2=len(tflist)
    return qval, pvalVec, tfdbdisease, nCondVec, qval1, pvalVec1, tfdbgwas, nCondVec1, stat1, stat2, qvalTE, pvalVecTE, nCondVecTE, qvalTT, pvalVecTT, nCondVecTT, tftissueex, tftissuetar

def enrichCmapReg(gene,sampleGenesUp,sampleGenesDown,brd):
    print('Reading drug database')
    #db         = pd.read_csv('cmapreg.csv', header=None,dtype=np.float64)
    if gene==1:
	    sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapreg.npz')
    elif gene==0:
        sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapregtf.npz')

	#sparse_matrix = scipy.sparse.load_npz(sys.argv[1]) #('sparse_cmapreg.npz')
	# None of python's sparse libraries allow storing colnames and rownames so they have to be maintained separetaly
    if gene==1:
        genNames  = pd.read_csv('src/clueReg/data/geneNames.csv',header=None) #'geneNames.csv'
    elif gene==0:
        genNames    = pd.read_csv('src/clueReg/data/tfNames.csv',header=None) #'geneNames.csv'
    drugDF = pd.read_csv('src/clueReg/data/drugNamesAug.csv', header=0,index_col=0)
    drugNames = drugDF.iloc[:,0]
    #drugNames  = pd.read_csv('src/cluereg/data/drugNames.csv',header=None)
    #geneNames  = pd.read_csv(sys.argv[2],header=None) #'geneNames.csv'
    #drugNames  = pd.read_csv(sys.argv[3],header=None) #'drugNames.csv'
    #db.columns = drugNames
    #geneNames  = geneNames.append(geneNames)

	# Save to sparse
	#sparse_matrix = sp.sparse.csc_matrix(db)
	#sp.sparse.save_npz('sparse_cmapreg.npz', sparse_matrix)

    # Read genes
    #sampleGenesUp  = pd.read_csv('src/cluereg/data/sampleUp.csv',header=None,dtype=str) #'sampleUp.csv'
    #sampleGenesDown= pd.read_csv('src/cluereg/data/sampleDown.csv',header=None,dtype=str) #'sampleDown.csv'
    #sampleGenesUp  = pd.read_csv(sys.argv[4],header=None,dtype=str) #'sampleUp.csv'
	#sampleGenesDown= pd.read_csv(sys.argv[5],header=None,dtype=str) #'sampleDown.csv'
    print(str(len(sampleGenesUp)) + ' Genes are Up')
    print(str(len(sampleGenesDown)) + ' Genes are Down')

    # Construct input vector
    print('Computing enrichment score to ' + str(len(drugNames)) + ' drugs')
    intersectUp     = np.array(np.in1d(genNames,sampleGenesUp) ,dtype=int)
    intersectDown   = np.array(np.in1d(genNames,sampleGenesDown),dtype=int)
    intersectUpOv   = np.concatenate([intersectUp, intersectUp])
    intersectDownOv = np.concatenate([intersectDown, intersectDown])

    # Compute overlap
    overlap         = intersectDownOv * sparse_matrix -intersectUpOv * sparse_matrix

    # Compute cosine similarity
    inputSig = intersectUp-intersectDown
    if gene==1:
        sparse_matrix_combined = sparse_matrix[:12282,:] + sparse_matrix[12282:,:]
    elif gene==0:
        sparse_matrix_combined = sparse_matrix[:644, :] + sparse_matrix[644:, :]
    cosDist  = cosine_similarity(inputSig.reshape(1,-1), sparse_matrix_combined.transpose())
    cosDist  = cosDist.transpose()
    cosDist  = np.concatenate( cosDist, axis=0 )

    # print results
    indSort  = np.argsort(overlap)
    #d = {'overlapScore': overlap[list(reversed(indSort))], 'cosine similarity': cosDist[list(reversed(indSort))] }
    #res = pd.DataFrame(data=d)
    #res.index = drugNames.iloc[list(reversed(indSort))]
    #res.to_csv('results.csv')

    #print('Results written to results.csv')

	# post to API
	#max_display = 100
	#for i in range(max_display):
		#payload = {'drug':drugNames.iloc[indSort[i]],'cosine':round(cosDist[indSort[i]],4),'overlap':overlap[indSort[i]]}
		#r = requests.put('http://localhost:8000/api/v1/drugresultup/' + str(i+1) + '/', data=payload)
		#print(r.status_code)

	#for i in range(max_display):
	        #payload = {'drug':drugNames.iloc[indSort[-1-i]],'cosine':round(cosDist[indSort[-1-i]],4),'overlap':overlap[indSort[-1-i]]}
	        #r = requests.put('http://localhost:8000/api/v1/drugresultdown/' + str(i+1) + '/', data=payload)
	        #print(r.status_code)

	# stats about query
    stat1=len(sampleGenesUp)
    stat2=len(sampleGenesDown)
    stat3=np.count_nonzero(intersectUp)
    stat4=np.count_nonzero(intersectDown)
    if brd=='on':
        indBrd=[False if d[0:4]=='BRD-' else True for d in drugNames]
        drugNames= drugNames[indBrd]
        drugNames.index=list(range(0,len(drugNames)))
        cosDist  = cosDist[indBrd]
        overlap  = overlap[indBrd]
        indSort  = np.argsort(overlap)
        drugDF   = drugDF.iloc[indBrd]
    return drugNames, cosDist, overlap, indSort, stat1, stat2, stat3, stat4, drugDF
