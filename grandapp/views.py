from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core import serializers
from .models import Cell, Disease, Cancer
from .models import Druglanding, DrugResultUp, DrugResultDown, Params, Tcgasample, Geosample, Genelanding
from .models import Tissue, Gwas, TissueEx, TissueTar, Tissuelanding, Tissuesample, Cancerlanding, Drugsample
from .models import Drugdesc, Breastsample, Cervixsample, Liversample, Ggbmd1sample, Ggbmd2sample, Ggnsample
from .models import Pancreassample, Drugcombsup, Drugcombsdown, Gobp, Cellpage, Celllanding, Cellsample
from .models import Gobpbygene, Gwascata, Gwascatabygene, Otterac, Pandaac, Dragonac, Sendto, Document, Tissueac
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from .forms import ContactForm, GeneForm, DiseaseForm, NetForm, BabelForm, TarForm, ClueForm, DocumentForm
from django.conf import settings
import os
import random
import time
from django.core import serializers

# file upload
from django.urls import reverse
from django.template import RequestContext

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
import statsmodels
import math

# for gene conversion
import mygene
import networkx as nx #for network analysis
mg = mygene.MyGeneInfo()

def convertGenelist(geneform,how='sym'):
    #geneform=str.split(geneform,'\r\n')
    # convert to gene symbols
    if how=='ens':
        geneSyms = mg.querymany(geneform , scopes=["ensemblgene", "symbol"], fields='ensembl.gene', species='human',as_dataframe=True)
    else:
        geneSyms = mg.querymany(geneform , scopes=["ensemblgene", "symbol"], fields='symbol', species='human',as_dataframe=True)
    #remove nonconverted genes
    if 'notfound' in geneSyms.columns:
        geneSyms=geneSyms[geneSyms.notfound != True]
    if how=='ens':
        geneform = geneSyms['ensembl.gene'].values
    else:
        geneform = geneSyms.symbol.values
    return geneform

def home(request):
    params  = Params.objects.filter(id=-1)
    print(params)
    return render(request, 'home.html', {'params':params})

def help(request):
    pandaac = Pandaac.objects.all()
    data = serializers.serialize("json", pandaac)
    dragonac = Dragonac.objects.all()
    datadrag = serializers.serialize("json", dragonac)
    return render(request, 'help.html',{'data':data,'datadrag':datadrag})

def download(request):
    return render(request, 'download.html')

def cell(request):
    cells = Cell.objects.all()
    cellspage = Cellpage.objects.all()
    data = serializers.serialize("json", cells)
    return render(request, 'cell.html', {'cells': cells,'data':data,'cellspage':cellspage})

def genes(request):
    geneslanding = Genelanding.objects.all()
    return render(request, 'genes.html',{'geneslanding':geneslanding})

def pathways(request):
    gobp = Gobp.objects.all()
    return render(request, 'pathways.html',{'gobp':gobp})

def gwas(request):
    return render(request, 'gwas.html')

def networksagg(request,slug):
    if request.method == 'GET':
        # network form
        form = NetForm({'dt':'no','topbottom':'Largest','nedges':100,'tfgenesel':'nosel'})
        nodes = pd.DataFrame(data=['TF','Gene'])
        nodes['id']   = [0,1]
        nodes.columns = ['label','id']
        if slug.split('_')[-1] == 'PUMA':
            nodes['group']= ['mir','exp'] 
        else:
            nodes['group']= ['tf','exp'] 
        edges= pd.DataFrame(data=[0.5])
        edges.columns= ['value']
        edges['from']= 0
        edges['to']  = 1
        edges['arrows']='to'
        nodes=nodes.to_json(orient='records')
        edges=edges.to_json(orient='records')
        # Targeting form 
        formtar = TarForm({'topbottomtar':'Largest','nedgestar':100,'topbottomtartf':'Largest','nedgestartf':100,'tfgeneseltar':'nosel'})
        clueform = ClueForm({'tfgeneselclue':'by gene'})
        dataset=''
    else:
        form = NetForm(request.POST, auto_id=True)
        # define form tar
        formtar = TarForm({'topbottomtar':'Largest','nedgestar':100,'topbottomtartf':'Largest','nedgestartf':100,'tfgeneseltar':'nosel'})
        clueform = ClueForm({'tfgeneselclue':'by gene'})
        if form.is_valid():
            nedges    = int(request.POST['nedges'])
            topbottom  = request.POST['topbottom']
            dt         = request.POST.get('dt', False)
            brd        = request.POST.get('brd', False)
            absval     = request.POST.get('absval', False)
            tfgenesel  = request.POST.get('tfgenesel', False)
            geneform   = request.POST.get('geneform', False)
            tfform     = request.POST.get('tfform', False)
            goform     = request.POST.get('goform', False)
            gwasform   = request.POST.get('gwasform', False)
            edgetargeting = request.POST.get('edgetargeting', False)
            if slug[0:3]=='ACH':
                form.fields['edgetargeting'].widget.attrs['disabled']    = 'disabled'
            print('The number of edges is',nedges)
            object_key=mapObjectkey(slug)
            df=fetchNetwork(object_key)
            if dt=='dtt':
                tftar  = df.sum(axis=1) 
                genetar= df.sum(axis=0)
            if dt=='dee':
                object_key=mapObjectkey(slug,modality='expression')
                deDf=fetchNetwork(object_key)
                deDfmean = deDf.values.mean()
                deDf = deDf.mean(axis=1)
            df.index.name='TF'
            df=selectgenes(df,tfgenesel,geneform,tfform,goform,gwasform)
            df=df.stack().reset_index().rename(columns={'TF':'source','level_1':'target', 0:'value'})
            if edgetargeting == 'on':
                object_key=mapObjectkey(slug,modality='motif')
                motif=fetchNetwork(object_key,how='motif')
                motif=motif[motif['value'] >0]
                df = pd.merge(df, motif, how ='left', on =['source', 'target'])
                df.columns=['source','target','value','dashes']
                df['dashes'] = df['dashes'].fillna(0)
            if absval == 'on':
                df['sigval']=df['value']
                df['value'] =np.abs(df['value'])
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
            if slug.split('_')[-1] == 'PUMA':
                nodes['group'] = ['mir']*len(b1) + ['exp']*len(b2)
            else:
                nodes['group'] = ['tf']*len(b1) + ['exp']*len(b2)
            titlearray = np.append(b1,b2)
            for i in range(len(titlearray)):
                origtitle=titlearray[i]
                if i < len(b1):
                    titlearray[i] = 'Regulator name: ' + titlearray[i] 
                else:
                    titlearray[i] = 'Gene name: ' + titlearray[i]
                try:
                    gobpbygene     = Gobpbygene.objects.get(gene=origtitle)
                    if i < len(b1):
                        titlearray[i] += '\nGO terms:' + gobpbygene.termlist
                    else:
                        titlearray[i] += '\nGO terms:' + gobpbygene.termlist
                except:
                    print('gene not found')
                try:
                    gwascatabygene     = Gwascatabygene.objects.get(gene=origtitle)
                    if i < len(b1):
                        titlearray[i] += '\nGWAS traits:' + gwascatabygene.termlist
                    else:
                        titlearray[i] += '\nGWAS traits:' + gwascatabygene.termlist
                except:
                    print('gene not found')
            nodes['title'] = titlearray
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
            if absval == 'on':
                edges['color'][df.sigval < 0] = 'red'
            elif absval == False:
                edges['color'][df.value < 0] = 'red'
            print(brd)
            if brd==False:
                del edges['value']
            elif brd=='on':
                edges.value   = np.abs(edges.value)
            if dt=='bc':
                # scale nodes by centrality
                nodes = buildNxGraph(nodes,edges,brd)
                print(nodes)
            # continue upping the df
            edges['arrows']= 'to'
            del edges['source'] 
            del edges['target']
            df=''
            nodes=nodes.to_json(orient='records')
            edges=edges.to_json(orient='records')
            form.save()
    cancerType=slug[:(len(slug)-8)].capitalize()
    try:
        if int(slug[len(slug)-1])==1:
            dataset='TCGA'
        elif int(slug[len(slug)-1])==2:
            dataset='GEO'
        else:
            dataset=''
    except:
        dataset=''
    outputDict = {'cancerType': cancerType, 'dataset':dataset, 'netform':form, 'nodes':nodes, 'edges':edges, 'tarform':formtar, 'clueform':clueform, 'slug':slug}
    return render(request, 'networksagg.html', outputDict)

def upload(request):
    if request.method == 'GET':
        # doc form
        docform = DocumentForm()
        # network form
        form = NetForm({'dt':'no','topbottom':'Largest','nedges':100,'tfgenesel':'nosel'})
        formtar = TarForm({'topbottomtar':'Largest','nedgestar':100,'topbottomtartf':'Largest','nedgestartf':100,'tfgeneseltar':'nosel'})
        nodes = pd.DataFrame(data=['TF','Gene'])
        nodes['id']   = [0,1]
        nodes.columns = ['label','id']
        nodes['shape']= ['triangle'] + ['circle']
        nodes['color']= ['#98c4e1']  + ['#d7cad1']
        nodes['x'] = [100,110]
        nodes['y'] = [200,200]
        edges= pd.DataFrame(data=[0.5])
        edges.columns= ['value']
        edges['from']= 0
        edges['to']  = 1
        edges['arrows']='to'
        nodes=nodes.to_json(orient='records')
        edges=edges.to_json(orient='records')
    else:
        activetab='uptab'
        # network form
        form = NetForm({'dt':'no','topbottom':'Largest','nedges':100,'tfgenesel':'nosel'})
        formtar = TarForm({'topbottomtar':'Largest','nedgestar':100,'topbottomtartf':'Largest','nedgestartf':100,'tfgeneseltar':'nosel'})
        nodes = pd.DataFrame(data=['TF','Gene'])
        nodes['id']   = [0,1]
        nodes.columns = ['label','id']
        nodes['shape']= ['triangle'] + ['circle']
        nodes['color']= ['#98c4e1']  + ['#d7cad1']
        edges= pd.DataFrame(data=[0.5])
        edges.columns= ['value']
        edges['from']= 0
        edges['to']  = 1
        edges['arrows']='to'
        nodes=nodes.to_json(orient='records')
        edges=edges.to_json(orient='records')
        docform = DocumentForm(request.POST, request.FILES)
        if docform.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            slug   = random.randint(1,1000000)
            newdoc.idd=slug
            newdoc.save()
            #df=pd.read_csv('./' + newdoc.docfile.url)
            # Redirect to the document list after POST
            return redirect('/ownnet/'+str(slug)+'/')
    outputDict = {'netform':form,'nodes':nodes,'edges':edges, 'docform': docform, 'activetab':activetab, 'formtar':formtar}
    return render(request, 'ownnet.html', outputDict)

def ownnet(request,slug):
    if request.method == 'GET':
        activetab='uptab'
        # network form
        docform  = DocumentForm()
        documents= Document.objects.all()
        form  = NetForm({'dt':'no','topbottom':'Largest','nedges':100,'tfgenesel':'nosel'})
        nodes = pd.DataFrame(data=['TF','Gene'])
        nodes['id']   = [0,1]
        nodes.columns = ['label','id']
        nodes['shape']= ['triangle'] + ['circle']
        nodes['color']= ['#98c4e1']   + ['#d7cad1']
        nodes['x'] = [100,110]
        nodes['y'] = [200,200]
        edges= pd.DataFrame(data=[0.5])
        edges.columns= ['value']
        edges['from']= 0
        edges['to']  = 1
        edges['arrows']='to'
        nodes=nodes.to_json(orient='records')
        edges=edges.to_json(orient='records')
        # Targeting form 
        formtar = TarForm({'topbottomtar':'Largest','nedgestar':100,'topbottomtartf':'Largest','nedgestartf':100,'tfgeneseltar':'nosel'})
        clueform = ClueForm({'tfgeneselclue':'by gene'})
    else:
        activetab='nettab'
        docform   = DocumentForm()
        documents = Document.objects.get(idd=int(slug))
        df        = pd.read_csv('./' + documents.docfile.url,index_col=0,sep=',')
        documents= Document.objects.all()
        form      = NetForm(request.POST, auto_id=True)
        # define form tar
        formtar  = TarForm({'topbottomtar':'Largest','nedgestar':100,'topbottomtartf':'Largest','nedgestartf':100,'tfgeneseltar':'nosel'})
        clueform = ClueForm({'tfgeneselclue':'by gene'})
        if form.is_valid():
            seconds = time.time()
            nedges    = int(request.POST['nedges'])
            topbottom  = request.POST['topbottom']
            dt         = request.POST.get('dt', False)
            brd        = request.POST.get('brd', False)
            absval     = request.POST.get('absval', False)
            tfgenesel  = request.POST.get('tfgenesel', False)
            geneform   = request.POST.get('geneform', False)
            tfform     = request.POST.get('tfform', False)
            goform     = request.POST.get('goform', False)
            gwasform   = request.POST.get('gwasform', False)
            print('The number of edges is',nedges)
            print(brd)
            #df = pd.read_csv('/Users/mab8354/Colon_cancer_TCGA.csv',index_col=0,sep=',')
            if dt=='dtt':
                tftar  = df.sum(axis=1) 
                genetar= df.sum(axis=0)
            if dt=='dee':
                deDf = pd.read_csv('/Users/mab8354/cancer_colon_expression_tcga.txt',index_col=0,sep='\t')
                deDfmean = deDf.values.mean()
                deDf = deDf.mean(axis=1)
            df=selectgenes(df,tfgenesel,geneform,tfform,goform,gwasform)
            # Rename then name of the index column
            df.index.name='TF'
            df=df.stack().reset_index().rename(columns={'TF':'source','level_1':'target', 0:'value'})
            if absval == 'on':
                df['sigval']=df['value']
                df['value'] =np.abs(df['value'])
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
            titlearray = np.append(b1,b2)
            for i in range(len(titlearray)):
                origtitle=titlearray[i]
                if i < len(b1):
                    titlearray[i] = 'Regulator name: ' + titlearray[i] 
                else:
                    titlearray[i] = 'Gene name: ' + titlearray[i]
                try:
                    gobpbygene     = Gobpbygene.objects.get(gene=origtitle)
                    if i < len(b1):
                        titlearray[i] += '\nGO terms:' + gobpbygene.termlist
                    else:
                        titlearray[i] += '\nGO terms:' + gobpbygene.termlist
                except:
                    print('gene not found')
                try:
                    gwascatabygene     = Gwascatabygene.objects.get(gene=origtitle)
                    if i < len(b1):
                        titlearray[i] += '\nGWAS traits:' + gwascatabygene.termlist
                    else:
                        titlearray[i] += '\nGWAS traits:' + gwascatabygene.termlist
                except:
                    print('gene not found')
            nodes['title'] = titlearray
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
            if absval == 'on':
                edges['color'][df.sigval < 0] = 'red'
            elif absval == False:
                edges['color'][df.value < 0] = 'red'
            print(brd)
            if brd==False:
                del edges['value']
            elif brd=='on':
                edges.value   = np.abs(edges.value)
            if dt=='bc':
                # scale nodes by centrality
                nodes = buildNxGraph(nodes,edges,brd)
                print(nodes)
            # continue upping the df
            edges['arrows']= 'to'
            del edges['source'] 
            del edges['target']
            df=''
            nodes=nodes.to_json(orient='records')
            edges=edges.to_json(orient='records')
            seconds2 = time.time()
            print(seconds2-seconds)
            form.save()
    outputDict = {'netform':form, 'nodes':nodes, 'edges':edges, 'tarform':formtar, 'clueform':clueform,'docform':docform,'slug':int(slug), 'documents':documents, 'activetab':activetab}
    return render(request, 'ownnet.html', outputDict)


def cluesubmit(request,slug):
    if request.method == 'GET':
        form2     = TarForm({'topbottomtar':'Largest','nedgestar':100,'topbottomtartf':'Largest','nedgestartf':100})
        netform  = NetForm({'dt':'no','topbottom':'Largest','nedges':100,'tfgenesel':'nosel'})
        clueform = ClueForm({'tfgeneselclue':'by gene'})
    else:
        clueform = ClueForm(request.POST, auto_id=True)
        form2     = TarForm({'topbottomtar':'Largest','nedgestar':100,'topbottomtartf':'Largest','nedgestartf':100})
        netform  = NetForm({'dt':'no','topbottom':'Largest','nedges':100,'tfgenesel':'nosel'})
        if clueform.is_valid():
            topbottom  = request.POST['tfgeneselclue']
            up,down='',''
            if topbottom=='by gene':
                tarsense='Gene targeting'
                sendto = Sendto.objects.get(idd=2) # first cancel TFs
                sendto.preload = 0
                sendto.save()
                sendto = Sendto.objects.get(idd=1) # then fecth genes
                if sendto.preload == 1:
                    up=sendto.genelistup
                    down=sendto.genelistdown
            elif topbottom=='by tf':   
                tarsense='TF targeting'
                sendto = Sendto.objects.get(idd=1) # first cancel genes
                sendto.preload = 0
                sendto.save()
                sendto = Sendto.objects.get(idd=2) # then fetch TFs
                if sendto.preload == 1: 
                    up=sendto.genelistup
                    down=sendto.genelistdown
            form = GeneForm({'contentup':up,'contentdown':down,'tfgene':tarsense}, auto_id=True)
    cancerType=slug[:(len(slug)-8)].capitalize()
    try:
        if int(slug[len(slug)-1])==1:
            dataset='TCGA'
        elif int(slug[len(slug)-1])==2:
            dataset='GEO'
        else:
            dataset=''
    except:
        dataset=''
    outputDict = {'cancerType': cancerType, 'dataset':dataset, 'netform':netform, 'tarform':form2, 'clueform':clueform, 'geneform':form}
    return render(request,'analysis.html',outputDict)

def taragg(request,slug):
    activetab='tar'
    if request.method == 'GET':
        form = TarForm({'topbottomtar':'Largest','nedgestar':100,'topbottomtartf':'Largest','nedgestartf':100})
        netform = NetForm({'dt':'no','topbottom':'Largest','nedges':100,'tfgenesel':'nosel'})
        clueform = ClueForm({'tfgeneselclue':'by gene'})
    else:
        form = TarForm(request.POST, auto_id=True)
        netform = NetForm({'dt':'no','topbottom':'Largest','nedges':100,'tfgenesel':'nosel'})
        clueform = ClueForm({'tfgeneselclue':'by gene'})
        tfgeneseltar  = request.POST.get('tfgeneseltar', False)
        geneformtar   = request.POST.get('geneformtar', False)
        goformtar     = request.POST.get('goformtar', False)
        gwasformtar   = request.POST.get('gwasformtar', False)
        if form.is_valid():
            absvaltar      = request.POST.get('absvaltar', False)
            absvaltartf    = request.POST.get('absvaltartf', False)
            topbottomtar   = request.POST['topbottomtar']
            topbottomtartf = request.POST['topbottomtartf']
            nedgestar      = int(request.POST['nedgestar'])
            nedgestartf    = int(request.POST['nedgestartf'])
            # fetch network
            object_key = 'cancer/colon_cancer/networks/panda/Colon_cancer_TCGA.csv'#object_key=mapObjectkey(slug)
            df=fetchNetwork(object_key)
            print(df)
            genetarscore= computetargeting(df,absvaltar,topbottomtar,nedgestar,'gene',tfgeneseltar,geneformtar,goformtar,gwasformtar)
            tftarscore  = computetargeting(df,absvaltartf,topbottomtartf,nedgestartf,'tf',tfgeneseltar,geneformtar,goformtar,gwasformtar)
            upgenes     = genetarscore[genetarscore['tar'] > 0]
            downgenes   = genetarscore[genetarscore['tar'] < 0]
            upgenestf   = tftarscore[tftarscore['tar'] > 0]
            downgenestf = tftarscore[tftarscore['tar'] < 0]
            # populate send to enrichment button
            sendto = Sendto.objects.get(idd=0)
            sendto.preload = 1
            sendto.genelistup='\n'.join(tftarscore['TF'].values)
            sendto.save()
            sendto = Sendto.objects.get(idd=1) # genes
            sendto.preload = 1 
            sendto.genelistup='\n'.join(upgenes['index'].values)
            sendto.genelistdown='\n'.join(downgenes['index'].values)
            sendto.save()
            sendto = Sendto.objects.get(idd=2) # tfs
            sendto.preload = 1
            sendto.genelistup='\n'.join(upgenestf['TF'].values)
            sendto.genelistdown='\n'.join(downgenestf['TF'].values)
            sendto.save()
            # trasnform df to json
            tftarscore=tftarscore.to_json(orient='records')
            genetarscore=genetarscore.to_json(orient='records')
        else:
            print('invalid form!')
    cancerType=slug[:(len(slug)-8)].capitalize()
    try:
        if int(slug[len(slug)-1])==1:
            dataset='TCGA'
        elif int(slug[len(slug)-1])==2:
            dataset='GEO'
        else:
            dataset=''
    except:
        dataset=''
    print('slug is')
    #slug=int(slug)
    print(slug)
    outputDict = {'cancerType': cancerType, 'dataset':dataset, 'tarform':form,'activetab':activetab, 'netform':netform, 'tftarscore':tftarscore, 'genetarscore':genetarscore, 'clueform':clueform, 'slug':slug}
    page='networksagg.html'
    return render(request, page, outputDict)

def owntaragg(request,slug):
    activetab='tar'
    if request.method == 'GET':
        form = TarForm({'topbottomtar':'Largest','nedgestar':100,'topbottomtartf':'Largest','nedgestartf':100})
        netform = NetForm({'dt':'no','topbottom':'Largest','nedges':100,'tfgenesel':'nosel'})
        clueform = ClueForm({'tfgeneselclue':'by gene'})
    else:
        nodes = pd.DataFrame(data=['TF','Gene'])
        nodes['id']   = [0,1]
        nodes.columns = ['label','id']
        nodes['shape']= ['triangle'] + ['circle']
        nodes['color']= ['#98c4e1']   + ['#d7cad1']
        nodes['x'] = [100,110]
        nodes['y'] = [200,200]
        edges= pd.DataFrame(data=[0.5])
        edges.columns= ['value']
        edges['from']= 0
        edges['to']  = 1
        edges['arrows']='to'
        nodes=nodes.to_json(orient='records')
        edges=edges.to_json(orient='records')
        form = TarForm(request.POST, auto_id=True)
        docform   = DocumentForm()
        netform = NetForm({'dt':'no','topbottom':'Largest','nedges':100,'tfgenesel':'nosel'})
        clueform = ClueForm({'tfgeneselclue':'by gene'})
        tfgeneseltar  = request.POST.get('tfgeneseltar', False)
        geneformtar   = request.POST.get('geneformtar', False)
        goformtar     = request.POST.get('goformtar', False)
        gwasformtar   = request.POST.get('gwasformtar', False)
        if form.is_valid():
            absvaltar      = request.POST.get('absvaltar', False)
            absvaltartf    = request.POST.get('absvaltartf', False)
            topbottomtar   = request.POST['topbottomtar']
            topbottomtartf = request.POST['topbottomtartf']
            nedgestar      = int(request.POST['nedgestar'])
            nedgestartf    = int(request.POST['nedgestartf'])
            # fetch network
            documents = Document.objects.get(idd=int(slug))
            df        = pd.read_csv('./' + documents.docfile.url,index_col=0,sep=',')
            documents = Document.objects.all()
            genetarscore= computetargeting(df,absvaltar,topbottomtar,nedgestar,'gene',tfgeneseltar,geneformtar,goformtar,gwasformtar)
            tftarscore  = computetargeting(df,absvaltartf,topbottomtartf,nedgestartf,'tf',tfgeneseltar,geneformtar,goformtar,gwasformtar)
            tftarscore.columns.values[0]  = 'TF'
            genetarscore.columns.values[0]= 'index'
            upgenes     = genetarscore[genetarscore['tar'] > 0]
            downgenes   = genetarscore[genetarscore['tar'] < 0]
            upgenestf   = tftarscore[tftarscore['tar'] > 0]
            downgenestf = tftarscore[tftarscore['tar'] < 0]
            # populate send to enrichment button
            sendto = Sendto.objects.get(idd=0)
            sendto.preload = 1
            sendto.genelistup='\n'.join(tftarscore['TF'].values)
            sendto.save()
            sendto = Sendto.objects.get(idd=1) # genes
            sendto.preload = 1 
            sendto.genelistup='\n'.join(upgenes['index'].values)
            sendto.genelistdown='\n'.join(downgenes['index'].values)
            sendto.save()
            sendto = Sendto.objects.get(idd=2) # tfs
            sendto.preload = 1
            sendto.genelistup='\n'.join(upgenestf['TF'].values)
            sendto.genelistdown='\n'.join(downgenestf['TF'].values)
            sendto.save()
            # trasnform df to json
            tftarscore=tftarscore.to_json(orient='records')
            genetarscore=genetarscore.to_json(orient='records')
        else:
            print('invalid form!')
    cancerType=slug[:(len(slug)-8)].capitalize()
    if int(slug[len(slug)-1])==1:
        dataset='TCGA'
    elif int(slug[len(slug)-1])==2:
        dataset='GEO'
    else:
        dataset=''
    slug=int(slug)
    outputDict = {'nodes':nodes, 'edges':edges, 'netform':netform, 'tarform':form, 'clueform':clueform,'docform':docform,'slug':int(slug), 'documents':documents, 'activetab':activetab, 'tftarscore':tftarscore, 'genetarscore':genetarscore}
    page='ownnet.html'
    return render(request, page, outputDict)

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
         sendto = Sendto.objects.get(idd=0)
         if sendto.preload == 1:
            form = DiseaseForm({'content':sendto.genelistup})
            # remove preload
            sendto.preload=0
            sendto.genelistup=''
            sendto.genelistdown=''
            sendto.save()
         else:
            form = DiseaseForm()
    else:
         form = DiseaseForm(request.POST, auto_id=True)
         if form.is_valid():
             content   = request.POST['content']
             data = content.split('\r\n')
             data = list(filter(None, data))
             data = convertGenelist(data)
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

def tissue(request):
    tissues = Tissue.objects.all()
    tissuesfil = Tissue.objects.filter(tool3='LIONESS')
    data = serializers.serialize("json", tissuesfil)
    tissueac = Tissueac.objects.all()
    datadrag = serializers.serialize("json", tissueac)
    print(tissueac)
    return render(request, 'tissues.html', {'tissues': tissues, 'data': data, 'datadrag':datadrag})

def babelomic(request):
    if request.method == 'GET':
        form = BabelForm({'topbottom':'Largest','nedges':70,'mir':'on'})
        nodes = pd.DataFrame(data=['CNV','Methylation','Histone marks','miRNA','Gene','Protein','Metabolite','Drug','Dependency'])
        nodes['id']    = [0,1,2,3,4,5,6,7,8]
        nodes.columns  = ['label','id']
        nodes['group'] = ['cnv','methyl','hm','mir','exp','prot','met','drugs','dep'] 
        edges= pd.DataFrame(data=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5])
        edges.columns  = ['value']
        edges['from']  = [0,1,2,3,4,5,5,5]
        edges['to']    = [4,4,4,4,5,6,7,8]
        edges['arrows']= 'to'
        nodes=nodes.to_json(orient='records')
        edges=edges.to_json(orient='records')
    else:
        form = BabelForm(request.POST, auto_id=True)
        print(form.is_valid())
        if form.is_valid():
            # Read form
            nedges    = int(request.POST['nedges'])
            topbottom = request.POST['topbottom']
            agg       = request.POST.get('agg', False)
            exp       = request.POST.get('exp', False)
            methyl    = request.POST.get('methyl', False)
            cnv       = request.POST.get('cnv', False)
            hm        = request.POST.get('hm', False)
            prot      = request.POST.get('prot', False)
            met       = request.POST.get('met', False)
            dep       = request.POST.get('dep', False)
            mir       = request.POST.get('mir', False)
            absval    = request.POST.get('absval', False)
            gp        = request.POST.get('gp', False)
            allay     = request.POST.get('allay', False)
            connex = request.POST['connex']
            # Read data
            edges=pd.read_csv('data/finalMatEdges.csv',index_col=0)
            edges['absvalue']=np.abs(edges['value'])
            print(connex)
            print(gp)
            if gp=='on':
                form.fields['mir'].widget.attrs['disabled']    = 'disabled'
                form.fields['exp'].widget.attrs['disabled']    = 'disabled'
                form.fields['methyl'].widget.attrs['disabled'] = 'disabled'
                form.fields['prot'].widget.attrs['disabled']   = 'disabled'
                form.fields['met'].widget.attrs['disabled']    = 'disabled'
                form.fields['hm'].widget.attrs['disabled']     = 'disabled'
                form.fields['agg'].widget.attrs['disabled']    = 'disabled'
                form.fields['allay'].widget.attrs['disabled']  = 'disabled'
                form.fields['cnv'].widget.attrs['disabled']    = 'disabled'
                form.fields['dep'].widget.attrs['disabled']    = 'disabled'
                if connex=='Methylation':
                    methylEdges=edges[edges.sourcegroup=='methyl']
                    methylEdges=selectEdges(methylEdges,topbottom,nedges,absval)
                    expdf=findTarget(methylEdges,edges)
                    expEdges=selectEdges(expdf,topbottom,nedges,absval)
                    #print(expEdges)
                    protdf=findTarget(expEdges,edges)
                    protEdges=selectEdges(protdf,topbottom,nedges,absval)
                    #print(protEdges)
                    mirEdges=pd.DataFrame(data=[])
                elif connex=='Histone':
                    methylEdges=edges[edges.sourcegroup=='hm']
                    methylEdges=selectEdges(methylEdges,topbottom,nedges,absval)
                    expdf=findTarget(methylEdges,edges)
                    expEdges=selectEdges(expdf,topbottom,nedges,absval)
                    #print(expEdges)
                    protdf=findTarget(expEdges,edges)
                    protEdges=selectEdges(protdf,topbottom,nedges,absval)
                    #print(protEdges)
                    mirEdges=pd.DataFrame(data=[])
                elif connex=='CNV':
                    methylEdges=edges[edges.sourcegroup=='cnv']
                    methylEdges=selectEdges(methylEdges,topbottom,nedges,absval)
                    expdf=findTarget(methylEdges,edges)
                    expEdges=selectEdges(expdf,topbottom,nedges,absval)
                    #print(expEdges)
                    protdf=findTarget(expEdges,edges)
                    protEdges=selectEdges(protdf,topbottom,nedges,absval)
                    #print(protEdges)
                    mirEdges=pd.DataFrame(data=[])
                elif connex=='miRNA':
                    mirEdges=edges[edges.sourcegroup=='mir']
                    mirEdges=selectEdges(mirEdges,topbottom,nedges,absval)
                    expdf=findTarget(mirEdges,edges)
                    expEdges=selectEdges(expdf,topbottom,nedges,absval)
                    #print(expEdges)
                    protdf=findTarget(expEdges,edges)
                    protEdges=selectEdges(protdf,topbottom,nedges,absval)
                    #print(protEdges)
                    methylEdges=pd.DataFrame(data=[])
                elif connex=='mRNA':
                    #down
                    expEdges=edges[edges.targetgroup=='exp']
                    expEdges=selectEdges(expEdges,topbottom,nedges,absval)
                    #up
                    protEdges=edges[edges.sourcegroup=='exp']
                    protEdges=selectEdges(protEdges,topbottom,nedges,absval)
                    expdf=findTarget(protEdges,edges)
                    methylEdges=selectEdges(expdf,topbottom,nedges,absval)
                    mirEdges=pd.DataFrame(data=[])
                elif connex=='Protein':
                    protEdges=edges[edges.sourcegroup=='prot']
                    protEdges=selectEdges(protEdges,topbottom,nedges,absval)
                    expEdges=edges[edges.targetgroup=='prot']
                    expEdges=selectEdges(expEdges,topbottom,nedges,absval)
                    expdf=findTarget(expEdges,edges,'source')
                    methylEdges=selectEdges(expdf,topbottom,nedges,absval)
                    mirEdges=pd.DataFrame(data=[])
                elif connex=='Metabolism':
                    protEdges=edges[edges.targetgroup=='met']
                    protEdges=selectEdges(protEdges,topbottom,nedges,absval)
                    protdf=findTarget(protEdges,edges,'source')
                    expEdges=selectEdges(protdf,topbottom,nedges,absval)
                    expdf=findTarget(expEdges,edges,'source')
                    methylEdges=selectEdges(expdf,topbottom,nedges,absval)
                    mirEdges=pd.DataFrame(data=[])
                elif connex=='Drugs':
                    protEdges=edges[edges.targetgroup=='drugs']
                    protEdges=selectEdges(protEdges,topbottom,nedges,absval)
                    protdf=findTarget(protEdges,edges,'source')
                    expEdges=selectEdges(protdf,topbottom,nedges,absval)
                    expdf=findTarget(expEdges,edges,'source')
                    methylEdges=selectEdges(expdf,topbottom,nedges,absval)
                    mirEdges=pd.DataFrame(data=[])
                elif connex=='Dependency':
                    protEdges=edges[edges.targetgroup=='dep']
                    protEdges=selectEdges(protEdges,topbottom,nedges,absval)
                    protdf=findTarget(protEdges,edges,'source')
                    expEdges=selectEdges(protdf,topbottom,nedges,absval)
                    expdf=findTarget(expEdges,edges,'source')
                    methylEdges=selectEdges(expdf,topbottom,nedges,absval)
                    mirEdges=pd.DataFrame(data=[])
                edges=pd.concat((methylEdges,mirEdges,expEdges,protEdges))
                print(edges)
            elif gp==False:
                if agg==False:
                    if (hm=='on') | (allay=='on'):
                        hmEdges=edges[edges.sourcegroup=='hm']
                        hmEdges=selectEdges(hmEdges,topbottom,nedges,absval)
                    elif hm==False: 
                        hmEdges=pd.DataFrame(data=[])
                    if (cnv=='on') | (allay=='on'):
                        cnvEdges=edges[edges.sourcegroup=='cnv']
                        cnvEdges=selectEdges(cnvEdges,topbottom,nedges,absval)
                    elif cnv==False: 
                        cnvEdges=pd.DataFrame(data=[])
                    if (methyl=='on') | (allay=='on'):
                        methylEdges=edges[edges.sourcegroup=='methyl']
                        methylEdges=selectEdges(methylEdges,topbottom,nedges,absval)
                    elif methyl==False: 
                        methylEdges=pd.DataFrame(data=[])
                    if (mir=='on') | (allay=='on'):
                        mirEdges=edges[edges.sourcegroup=='mir']
                        mirEdges=selectEdges(mirEdges,topbottom,nedges,absval)
                    elif mir==False:
                        mirEdges=pd.DataFrame(data=[])
                    if (exp=='on') | (allay=='on'):
                        expEdges=edges[edges.sourcegroup=='exp']
                        expEdges=selectEdges(expEdges,topbottom,nedges,absval)
                    elif exp==False:
                        expEdges=pd.DataFrame(data=[])
                    if (prot=='on') | (allay=='on'):
                        protEdges=edges[edges.sourcegroup=='prot']
                        protEdges=selectEdges(protEdges,topbottom,nedges,absval)
                    elif prot==False:
                        protEdges=pd.DataFrame(data=[])
                    if allay=='on':
                        form.fields['agg'].widget.attrs['disabled']  = 'disabled'
                    if (methyl==False) & (mir==False) & (allay==False) & (exp==False) & (prot==False) & (cnv==False) & (hm==False):
                        agg='on'
                        form.fields['agg'].widget.attrs['checked']    = 'checked'
                    else:
                        edges=pd.concat((cnvEdges,methylEdges,mirEdges,expEdges,protEdges,hmEdges))
                if agg=='on':
                    form.fields['mir'].widget.attrs['disabled']    = 'disabled'
                    form.fields['exp'].widget.attrs['disabled']    = 'disabled'
                    form.fields['methyl'].widget.attrs['disabled'] = 'disabled'
                    form.fields['prot'].widget.attrs['disabled']   = 'disabled'
                    form.fields['met'].widget.attrs['disabled']    = 'disabled'
                    form.fields['hm'].widget.attrs['disabled']     = 'disabled'
                    form.fields['allay'].widget.attrs['disabled']  = 'disabled'
                    form.fields['cnv'].widget.attrs['disabled']    = 'disabled'
                    form.fields['dep'].widget.attrs['disabled']    = 'disabled'
                    if absval=='on':
                        edges=edges.sort_values(by=['absvalue'])
                    elif absval==False:
                        edges=edges.sort_values(by=['value'])
                    if topbottom=='Smallest':
                        edges=edges.iloc[0:nedges,]
                    elif topbottom=='Largest':
                        edges=edges.iloc[(len(edges)-nedges):len(edges),]
            print('The number of edges is',edges.shape)
            b1, c1 = np.unique(pd.concat((edges.source,edges.target)), return_inverse=True)    
            #b2, c2 = np.unique(edges.target, return_inverse=True)  
            nodes = pd.DataFrame(data=b1)
            nodes['id']    = list(range(0,len(b1)))
            nodes.columns  = ['label','id']
            aa,bb = np.unique(c1, return_index=True)
            #aa1,bb1= np.unique(c2, return_index=True)
            vv = pd.concat((edges.sourcegroup,edges.targetgroup))
            vv.index=range(0,len(vv))
            nodes['group'] = vv.iloc[bb].values
            edges['from']  = c1[:edges.shape[0]]
            edges['to']    = c1[edges.shape[0]:]
            edges['arrows']= 'to'
            edges['color'] = 'green'
            edges['color'][edges.value < 0] = 'red'
            edges['value'] = np.abs(edges['value'])
            del edges['source'] 
            del edges['target']
            del edges['absvalue']
            print(edges)
            nodes=nodes.to_json(orient='records')
            edges=edges.to_json(orient='records')
            form.save()
    outputDict = {'netform':form, 'nodes':nodes, 'edges':edges}
    return render(request, 'babelomic.html', outputDict)

def tissuelanding(request,slug):
    slug2=slug.replace('_',' ')[:-7]
    tissuelanding  = Tissuelanding.objects.filter(tissue=slug2)
    tissuesample   = Tissuesample.objects.filter(grdid=slug) 
    tissuelanding2 = Tissuelanding.objects.filter(tissue=slug2)
    nsamples = 0
    for model in tissuelanding2:
        if model.tool=='PANDA-LIONESS':
            nsamples = model.samples
    ndata,nagg=1,3
    data = serializers.serialize("json", tissuesample)
    name= 'yes'
    if slug in ['Lymphoblastoid_cell_line_tissue','Fibroblast_cell_line_tissue','Kidney_cortex_tissue','Minor_salivary_gland_tissue',
               'Ovary_tissue','Prostate_tissue','Testis_tissue','Uterus_tissue','Vagina_tissue']:
        name='no'
    return render(request, "tissueslanding.html", {'tissuelanding': tissuelanding, 'slug':slug,'tissuesample':tissuesample, 'name':name, 'data':data, 'ndata':ndata, 'nagg':nagg, 'nsamples':nsamples, 'slug2':slug2})

def cancer(request):
    cancer = Cancer.objects.all()
    return render(request, 'cancer.html', {'cancer': cancer})

def selectEdges(edges,topbottom,nedges,absval):
    if absval=='on':
        edges=edges.sort_values(by=['absvalue'])
    elif absval==False:
        edges=edges.sort_values(by=['value'])
    if topbottom=='Smallest':
        edges=edges.iloc[0:nedges,]
    elif topbottom=='Largest':
        edges=edges.iloc[(len(edges)-nedges):len(edges),]
    return edges

def findTarget(methylEdges,edges,source='target'):
    if source=='source':
        dd=np.unique(methylEdges.source)
        ss=np.in1d(edges.target, dd)
    elif source=='target':
        dd=np.unique(methylEdges.target)
        ss=np.in1d(edges.source, dd)
    expEdges=edges[ss]
    return expEdges

def cancerlanding(request,slug):
    cancerlanding = Cancerlanding.objects.filter(cancer=slug.replace('_',' '))
    data=''
    if slug in ['Cervix_cancer','Liver_cancer','Breast_cancer']:
        otterac = Otterac.objects.all()
        data = serializers.serialize("json", otterac)
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
                  'tcgasample':tcgasample, 'nsamples':nsamples,'ndata':ndata, 'nagg':nagg, 'data':data}
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

def celllanding(request,slug):
    tooldrag=''
    if slug == 'lcl':
        slug='Lymphoblastoid_cell_line_tissue'
        slugname = 'Lymphoblastoid cell line'
        celllanding = Tissuelanding.objects.filter(tissue=slug.replace('_',' ')[:-7])
        cellsample = Tissuesample.objects.filter(grdid=slug) 
        print(cellsample)
        nsamples,ndata,nagg=0,1,3
        data = serializers.serialize("json", cellsample)
        name,tool,slug='no','puma','lcl'
    elif slug == 'fibroblast_gtex':
        slug='Fibroblast_cell_line_tissue'
        slugname = 'Fibroblast cell line'
        celllanding = Tissuelanding.objects.filter(tissue=slug.replace('_',' ')[:-7])
        cellsample  = Tissuesample.objects.filter(grdid=slug) 
        print(cellsample)
        nsamples,ndata,nagg=0,1,3
        data = serializers.serialize("json", cellsample)
        name,tool,slug='no','puma','fibroblast_gtex'
    else:
        if len(slug.split('_')) > 1:
            slugname=slug.replace('_',' ')[:-7] + ' cancer'
        else:
            slugname=slug + ' cancer'
        tool=''
        name='yes'
        if slug == 'mirna':
            slugname='miRNA aggregate cancer'
            celllanding = Celllanding.objects.filter(tool='DRAGON')
            cellsample  = Cellsample.objects.filter(dummy='dragon')
            print(celllanding)
            nsamples,ndata,nagg=0,1,1
            tooldrag,name='yes','no'
        else:
            celllanding = Celllanding.objects.get(cancerref=slug)
            #initialize data variables
            nsamples,ndata,nagg=celllanding.samples,1,0
            print(slug)
            celllanding = Celllanding.objects.filter(cancerref=slug)
            obj = Celllanding.objects.get(cancerref=slug)
            slug2 = obj.cancer
            print(slug2)
            cellsample = Cellsample.objects.filter(disease=slug2).filter(presexp=1)
            print(cellsample)
        for cells in cellsample:
            try:
                cells.age=float(cells.age)
            except:
                cells.age='NA'
            try:
                cells.cas9act=float(cells.cas9act)
            except:
                cells.cas9act='NA'
            try:
                cells.mutrate=float(cells.mutrate)
            except:
                cells.mutrate='NA'
            try:
                cells.doublt=float(cells.doublt)
            except:
                cells.doublt='NA'
            cells.save()
        data = serializers.serialize("json", cellsample)
    returntupl = {'celllanding': celllanding, 'slug':slug, 
                  'nsamples':nsamples,'ndata':ndata, 'nagg':nagg, 'data':data, 'cellsample':cellsample, 'name':name, 'tool':tool, 'tooldrag':tooldrag, 'slugname':slugname}
    return render(request, "celllanding.html", returntupl)

def analysis(request):
    if request.method == 'GET':
        form = GeneForm({'tfgene':''}, auto_id=True)
        combin = False
    else:
         form = GeneForm(request.POST)
         if form.is_valid():
             contentup   = request.POST['contentup']
             contentdown = request.POST['contentdown']
             tfgene      = request.POST['tfgene']
             brd         = request.POST.get('brd', False)
             combin      = request.POST.get('combin', False)
             max_display = int(request.POST['ngenes'])
             if tfgene=='Gene targeting':
                data = contentup.split('\r\n')
                data = list(filter(None, data))
                data = convertGenelist(data,how='ens')
                sampleUp = pd.DataFrame(data, columns = ['Gene'])
                data = contentdown.split('\r\n')
                data = list(filter(None, data))
                data = convertGenelist(data,how='ens')
                sampleDown = pd.DataFrame(data, columns = ['Gene'])
             elif tfgene=='TF targeting':
                data = contentup.split('\r\n')
                data = list(filter(None, data))
                data = convertGenelist(data)
                sampleUp = pd.DataFrame(data, columns = ['Gene'])
                data = contentdown.split('\r\n')
                data = list(filter(None, data))
                data = convertGenelist(data)
                sampleDown = pd.DataFrame(data, columns = ['Gene'])
             try:
                 if tfgene=='Gene targeting':
                     gene=1
                 elif tfgene=='TF targeting':
                     gene=0
                 drugNames, cosDist, overlap, indSort, stat1, stat2, stat3, stat4, drugDF, resdfcombup, resdfcombdown = \
                            enrichCmapReg(gene,sampleUp,sampleDown,brd,max_display,combin)
                 if gene==0:
                     # load pvals
                     name='resDfTF'
                     c=np.append(indSort[0:max_display]+1,0)
                     d=np.append(indSort[-max_display:]+1,0)
                     pvalDfUp = loadPvals(d,name)
                     pvalDfDown = loadPvals(c,name)
                     # load tvals
                     name='resDfTF'
                     c=np.append(indSort[0:max_display]+1,0)
                     d=np.append(indSort[-max_display:]+1,0)
                     tvalDfUp = loadPvals(d,name,how='tau')
                     tvalDfDown = loadPvals(c,name,how='tau')
                 elif gene==1:
                     # load pvals
                     c=np.append(indSort[0:max_display]+1,0)
                     d=np.append(indSort[-max_display:]+1,0)
                     name='resDfGene'
                     pvalDfUp = loadPvals(d,name)
                     pvalDfDown = loadPvals(c,name)
                     # load tvals
                     c=np.append(indSort[0:max_display]+1,0)
                     d=np.append(indSort[-max_display:]+1,0)
                     name='resDfGene'
                     tvalDfUp = loadPvals(d,name,how='tau')
                     tvalDfDown = loadPvals(c,name,how='tau')
                 #max_display=100
                 randid      =random.randint(1,1000000)
                 counter= Params.objects.get(id=-1)
                 newID  = counter.genesupin % 10
                 i=0
                 pvalsUp,pvalsDown=[],[]
                 for i in range(max_display):
                     drug=DrugResultUp.objects.get(idd=i+1, nuser=newID)
                     # drug combs up
                     if combin=='on':
                        drugcombup=Drugcombsup.objects.get(idd=i+1, nuser=newID)
                        drugcombup.drug1 = resdfcombup['drug1'].iloc[i]
                        drugcombup.drug2 = resdfcombup['drug2'].iloc[i]
                        drugcombup.cosine= round(resdfcombup['cosine'].iloc[i],4)
                        drugcombup.abscosine= np.abs(drugcombup.cosine)
                        drugcombup.query = randid
                        drugcombup.save()
                     currDrugName = drugNames[indSort[i]]
                     drug.orig    = currDrugName
                     drug.drug    = currDrugName[0].upper() + currDrugName[1:]
                     drug.cosine  = round(cosDist[indSort[i]],4)
                     drug.pval    = np.sum( pvalDfUp.iloc[i,:] >= drug.cosine )/pvalDfUp.shape[1]
                     pvalsUp.append(drug.pval)
                     drug.tval    = round(np.sum( tvalDfUp.iloc[i,:] >= drug.cosine )/tvalDfUp.shape[1],4)
                     drug.overlap = overlap[indSort[i]]
                     drug.druglink= 'https://grand.networkmedicine.org/drugs/' + drug.drug + '-drug/'
                     drug.query   = randid
                     drug.altid           =drugDF.iloc[indSort[i],1]
                     drug.inchi_key_prefix=drugDF.iloc[indSort[i],5]
                     drug.inchi_key       =drugDF.iloc[indSort[i],6]
                     drug.canonical_smiles=drugDF.iloc[indSort[i],7]
                     drug.pubchem_cid     =drugDF.iloc[indSort[i],8]
                     # save 
                     drug.save()
                     drug=DrugResultDown.objects.get(idd=i+1, nuser=newID)
                     # drug combs down
                     if combin=='on':
                        drugcombdown=Drugcombsdown.objects.get(idd=i+1, nuser=newID)
                        drugcombdown.drug1 = resdfcombdown['drug1'].iloc[i]
                        drugcombdown.drug2 = resdfcombdown['drug2'].iloc[i]
                        drugcombdown.cosine= round(resdfcombdown['cosine'].iloc[i],4)
                        drugcombdown.abscosine= np.abs(drugcombdown.cosine)
                        drugcombdown.query = randid
                        drugcombdown.save()
                     currDrugName = drugNames[indSort[-1-i]]
                     drug.orig    = currDrugName
                     drug.drug    = currDrugName[0].upper() + currDrugName[1:]
                     drug.cosine  = round(cosDist[indSort[-1-i]],4)
                     drug.pval    = np.sum( pvalDfDown.iloc[i,:] <= drug.cosine )/pvalDfDown.shape[1]
                     drug.tval    = round(np.sum( tvalDfDown.iloc[i,:] <= drug.cosine )/tvalDfDown.shape[1],4)
                     pvalsDown.append(drug.pval)
                     drug.overlap = overlap[indSort[-1-i]]
                     drug.druglink= 'https://grand.networkmedicine.org/drugs/' + drug.drug + '-drug/'
                     drug.query   = randid
                     drug.altid           =drugDF.iloc[indSort[-1-i],1]
                     drug.inchi_key_prefix=drugDF.iloc[indSort[-1-i],5]
                     drug.inchi_key       =drugDF.iloc[indSort[-1-i],6]
                     drug.canonical_smiles=drugDF.iloc[indSort[-1-i],7]
                     drug.pubchem_cid     =drugDF.iloc[indSort[-1-i],8]
                     # save 
                     drug.save()
                     i+=1
                     #payload = {'drug':drugNames.iloc[indSort[-1-i]],'cosine':round(cosDist[indSort[-1-i]],4),'overlap':overlap[indSort[-1-i]]}
                 qvalsUp = statsmodels.stats.multitest.multipletests(pvalsUp, alpha=0.05) 
                 qvalsDown = statsmodels.stats.multitest.multipletests(pvalsDown, alpha=0.05) 
                 for i in range(max_display):
                     drug=DrugResultUp.objects.get(idd=i+1, nuser=newID)
                     drug.qval=round(qvalsUp[1][i],4)
                     drug.save()
                     drug=DrugResultDown.objects.get(idd=i+1, nuser=newID)
                     drug.qval=round(qvalsDown[1][i],4)
                     drug.save()
                 accessKey = randid
                 param  = Params.objects.get(id=newID)
                 param.genesupin   = stat1
                 param.genesdownin = stat2
                 param.genesup     = stat3
                 param.genesdown   = stat4
                 param.query       = randid
                 param.combin     = combin
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
    drugdowncomb = Drugcombsdown.objects.filter(query=id)
    data = serializers.serialize("json", drugdown)
    sense='reverse'
    return render(request, 'drugresult.html', {'params':params,'drugdown':drugdown,'id':id, 'data': data, 'sense':sense, 'drugdowncomb':drugdowncomb})

def drugresultsimilar(request, id):
    params = Params.objects.filter(query=id)
    drugup = DrugResultUp.objects.filter(query=id)
    drugupcomb = Drugcombsup.objects.filter(query=id)
    data = serializers.serialize("json", drugup)
    sense='similar'
    return render(request, 'drugresultsimilar.html', {'params':params,'drugup':drugup,'id':id, 'data': data, 'sense':sense, 'drugupcomb':drugupcomb})

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

def combDf(sparse_matrix_combined,max_display,drugNames,indSort,mode):
    if mode == 'up':
        sparse_matrix_combined = sparse_matrix_combined[:,indSort[0:max_display]]
        drugNamesComb = drugNames[indSort[0:max_display]]
    elif mode == 'down':
        sparse_matrix_combined = sparse_matrix_combined[:,indSort[-max_display:]]
        drugNamesComb = drugNames[indSort[-max_display:]]
    print('Computing combinations !')
    resmatcomb=[]
    for i in range(max_display-1):
        cosDistComb = cosine_similarity(np.transpose(sparse_matrix_combined[:,i]), np.transpose(sparse_matrix_combined[:,i+1:]))
        resmatcomb  = np.concatenate((resmatcomb,cosDistComb.flatten()))
    newcols=[]
    drug1,drug2=[],[]
    for i in range(max_display):
        for j in range(i+1,max_display):
            newcols.append(drugNamesComb.iloc[i] + '_' + drugNamesComb.iloc[j])
            drug1.append(drugNamesComb.iloc[i])
            drug2.append(drugNamesComb.iloc[j])
    resdfcomb=pd.DataFrame(data=resmatcomb, columns=['cosine'], index=newcols)
    resdfcomb['drug1']=drug1
    resdfcomb['drug2']=drug2
    resdfcomb['abscosine']=np.abs(resdfcomb['cosine'])
    resdfcomb = resdfcomb.sort_values(by=['abscosine'])
    print(resdfcomb)
    return resdfcomb

def enrichCmapReg(gene,sampleGenesUp,sampleGenesDown,brd,max_display,combin):
    print('Reading drug database')
    # init variables
    resdfcombup, resdfcombdown = [],[]
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

    # Print results
    indSort  = np.argsort(overlap)

    max_display=20 # combinations between the first 20 drugs
    if combin=='on':
        if brd==False:
            # Compute combinations
            resdfcombup   = combDf(sparse_matrix_combined,max_display,drugNames,indSort,mode='up')
            resdfcombdown = combDf(sparse_matrix_combined,max_display,drugNames,indSort,mode='down')  

	# Stats about query
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
        sparse_matrix_combined = sparse_matrix_combined[:,indBrd]
        if combin=="on":
            # Compute combinations
            resdfcombup   = combDf(sparse_matrix_combined,max_display,drugNames,indSort,mode='up')
            resdfcombdown = combDf(sparse_matrix_combined,max_display,drugNames,indSort,mode='down')  
    return drugNames, cosDist, overlap, indSort, stat1, stat2, stat3, stat4, drugDF, resdfcombup, resdfcombdown

def loadPvals(includedIndex,name,how='pval'):
    skiprowVecs   = []
    ndrugs=19792
    if how=='pval':
        addStr=''
    elif how=='tau':
        addStr='Tau'
    for i in range(ndrugs):
        if i not in includedIndex:
            skiprowVecs.append(i)
    a=pd.read_csv('data/'+name+addStr+'.csv',index_col=0,skiprows=skiprowVecs)
    return a

def buildNxGraph(nodes,edges,brd):
    G = nx.Graph()
    G.add_nodes_from(nodes['id'])
    for i in range(len(edges)):
        if brd=='on':
            G.add_edge(edges['from'].iloc[i], edges['to'].iloc[i], weight=edges['value'].iloc[i])
            nodesbs = nx.betweenness_centrality(G, weight='weight')
        elif brd==False:
            G.add_edge(edges['from'].iloc[i], edges['to'].iloc[i])
            nodesbs = nx.betweenness_centrality(G)
    dictlist=[]
    for key, value in nodesbs.items():
        temp = [key,value]
        dictlist.append(value)
    nodes['value']=dictlist
    return nodes

def computetargeting(df,absvaltartf,topbottomtartf,nedgestartf,how,tfgenesel,geneform,goform,gwasform):
    if how=='gene':
        # compute gene targeting descending order
        tftarscore=df.sum(axis=0).sort_values(axis=0,ascending=False)
    elif how=='tf':
        # compute tf targeting descending order
        tftarscore=df.sum(axis=1).sort_values(axis=0,ascending=False)
    # zscore
    tftarscore = (tftarscore - tftarscore.mean())/tftarscore.std(ddof=0)
    tftarscore=pd.DataFrame(data=tftarscore,columns=['tar'])
    tftarscore.reset_index(inplace=True)
    if how=='gene':
        tftarscore=selectgenestar(tftarscore,tfgenesel,geneform,goform,gwasform)
    if absvaltartf==False:
        if topbottomtartf=='Largest':
            tftarscore=tftarscore.iloc[0:nedgestartf]
        elif topbottomtartf=='Smallest':
            tftarscore=tftarscore.iloc[-nedgestartf:]
    elif absvaltartf=='on':
        tftarscore['abstar'] = np.abs(tftarscore['tar'])
        tftarscore=tftarscore.sort_values(by='abstar',ascending=False)
        if topbottomtartf=='Largest':
            tftarscore=tftarscore.iloc[0:nedgestartf]
        elif topbottomtartf=='Smallest':
            tftarscore=tftarscore.iloc[-nedgestartf:]
    return tftarscore

def selectgenes(df,tfgenesel,geneform,tfform,goform,gwasform):
    if tfgenesel=='by gene':
        geneform=str.split(geneform,'\r\n')
        try:
            geneform = convertGenelist(geneform)
            print(geneform)
            print( np.intersect1d(geneform,df.columns).size )
        except:
            print('no intersection')
        intergenes=np.intersect1d(geneform,df.columns)
        if intergenes.size > 0:
            df=df.loc[:,intergenes]
    elif tfgenesel=='by tf':
        tfform=str.split(tfform,'\r\n')
        # convert to gene symbols
        try:
            tfform=str.split(tfform,'\r\n')
            tfform = convertGenelist(tfform)
        except:
            print('no intersection')
        intertfs=np.intersect1d(tfform,df.index)
        if intertfs.size> 0:
            df=df.loc[intertfs]
    elif tfgenesel=='by GO':
        goform=str.split(goform,'\r\n')
        try:
            gobp  = Gobp.objects.get(goid=goform[0])
            genelist=str.split(gobp.genelist,',')
            intergo=np.intersect1d(genelist,df.columns)
            if intergo.size > 0:
                df=df.loc[:,intergo]
        except:
            print('no intersection')
    elif tfgenesel=='by GWAS':
        gwasform=str.split(gwasform,'\r\n')
        try:
            print(gwasform[0])
            gwascata  = Gwascata.objects.get(term=gwasform[0])
            genelist=str.split(gwascata.genelist,',')
            intergo=np.intersect1d(genelist,df.columns)
            if intergo.size > 0:
                df=df.loc[:,intergo]
        except:
            print('no intersection')
    return df

def fetchNetwork(object_key,how='net'):
    client = boto3.client('s3')
    bucket_name = 'granddb'
    csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    if how=='net':
        df = pd.read_csv(StringIO(csv_string),index_col=0,sep=',')
    elif how=='motif':
        df = pd.read_csv(StringIO(csv_string), sep='\t', header=None)
        df.columns=['source','target','value']
    return df

def selectgenestar(genetarscore,tfgenesel,geneform,goform,gwasform):
    if tfgenesel=='by gene':
        geneform=str.split(geneform,'\r\n')
        try:
            geneform = convertGenelist(geneform)
            print(geneform)
            print( np.intersect1d(geneform,genetarscore['index']).size )
        except:
            print('no intersection')
        print(geneform)
        intergenes=np.intersect1d(geneform,genetarscore['index'])
        print(genetarscore['index'])
        print(intergenes)
        if intergenes.size > 0:
            genetarscore = genetarscore.loc[genetarscore['index'].isin(intergenes)]
    elif tfgenesel=='by GO':
        goform=str.split(goform,'\r\n')
        try:
            gobp  = Gobp.objects.get(goid=goform[0])
            genelist=str.split(gobp.genelist,',')
            intergo=np.intersect1d(genelist,genetarscore['index'])
            if intergo.size > 0:
                genetarscore = genetarscore.loc[genetarscore['index'].isin(intergo)]
        except:
            print('no intersection')
    elif tfgenesel=='by GWAS':
        gwasform=str.split(gwasform,'\r\n')
        try:
            print(gwasform[0])
            gwascata  = Gwascata.objects.get(term=gwasform[0])
            genelist=str.split(gwascata.genelist,',')
            intergo=np.intersect1d(genelist,genetarscore['index'])
            if intergo.size > 0:
                genetarscore = genetarscore.loc[genetarscore['index'].isin(intergo)]
        except:
            print('no intersection')
    return genetarscore

def mapObjectkey(slug,modality='network'):
    if slug[0:3]=='ACH': #cell lines
        slug = str.replace(slug,'_','-')
        object_key = 'cells/networks/ccle/' + slug + '.csv'
        if modality=='expression':
            object_key='cells/expression/CCLE_expression_withinSample.csv'
    elif slug + '.csv' in ['Adipose_Subcutaneous.csv','Adipose_Visceral.csv','Adrenal_Gland.csv','Artery_Aorta.csv','Artery_Coronary.csv','Artery_Tibial.csv','Brain_Basal_Ganglia.csv','Brain_Cerebellum.csv','Brain_Other.csv','Breast.csv','Colon_Sigmoid.csv','Colon_Transverse.csv','Esophagus_Mucosa.csv','Esophagus_Muscularis.csv','Fibroblast_Cell_Line.csv','Gastroesophageal_Junction.csv','Heart_Atrial_Appendage.csv','Heart_Left_Ventricle.csv','Intestine_Terminal_Ileum.csv','Kidney_Cortex.csv','Liver.csv','Lung.csv','Lymphoblastoid_Cell_Line.csv','Minor_Salivary_Gland.csv','Ovary.csv','Pancreas.csv','Pituitary.csv','Prostate.csv','Skeletal_Muscle.csv','Skin.csv','Spleen.csv','Stomach.csv','Testis.csv','Thyroid.csv','Tibial_Nerve.csv','Uterus.csv','Vagina.csv','Whole_Blood.csv']: # tissues
        if modality == 'network':
            object_key = 'tissues/networks/' + slug + '.csv'
        elif modality=='expression':
            object_key = 'tissues/expression/' + slug + '.csv'
        elif modality=='motif':
            object_key = 'tissues/motif/tissues_motif.txt'
    elif slug.split('_')[4] == 'PUMA': # puma 
        if modality == 'network':
            object_key = 'tissues/networks/puma/' + slug + '.csv'
        elif modality=='expression':
            pumaslug=slug.split('_')
            a=pumaslug[:-2]
            a.append(pumaslug[-1])
            a='_'.join(a)
            object_key = 'tissues/expression/puma/' + a + '.csv'
        elif modality=='motif':
            pumaslug=slug.split('_')
            if pumaslug[-2] == 'miRanda':
                object_key =  'tissues/motif/tissue_MiRanda_prior.txt'
            elif pumaslug[-2] == 'TargetScan':
                object_key =  'tissues/motif/tissue_TargetScan_prior.txt'
    return object_key