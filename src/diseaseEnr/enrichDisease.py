import pandas as pd
import os
import scipy.stats as stats
import numpy as  np
import requests
from statsmodels.stats import multitest # for fdr correction

#Read query
tflist = pd.read_csv('src/diseaseEnr/sampleTFGWAS.csv',header=None)

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
for i in range(len(tfdbgwas)):
    payload = {'disease':tfdbgwas.iloc[i,0] ,'count':tfdbgwas.iloc[i,3],'intersect':nCondVec[i],'pval':round(pvalVec[i],5),'qval':round(qval[i],5)}
    r = requests.put('http://localhost:8000/api/v1/gwas/' + str(i+1) + '/', data=payload)


#2. Disease
tfdbdisease = pd.read_csv('src/diseaseEnr/TF-disease-data_Fig4_Disease.csv')

#Compute p-values
pvalVec = np.zeros(len(tfdbdisease))
nCondVec= np.zeros(len(tfdbdisease))
totPop  = 1639 #total number in population according to Lambert et al, Cell, 2018.
#totCond = np.zeros()#total number with condition in population
nSubset = len(tflist)#size of subset
#nCond   = #n condition in subset
for i in range(len(tfdbdisease)):
    totCond       = tfdbdisease.iloc[i,3]
    gt            = tfdbdisease.iloc[i, 4].split(',')[:-2]
    nCond         = len(set(gt).intersection(set(tflist.iloc[:, 0])))
    nCondVec[i]   = nCond
    pvalVec[i]    = stats.hypergeom.sf(nCond - 1,totPop,totCond,nSubset)

qval = multitest.fdrcorrection(pvalVec)
qval = qval[1]
for i in range(len(tfdbdisease)):
    payload = {'disease':tfdbdisease.iloc[i,0] ,'count':tfdbdisease.iloc[i,3],'intersect':nCondVec[i],'pval':round(pvalVec[i],5),'qval':round(qval[i],5)}
    r = requests.put('http://localhost:8000/api/v1/disease/' + str(i+1) + '/', data=payload)

#. Submission stats
stat1=len(set(alltfs.iloc[:,0]).intersection(set(tflist.iloc[:,0])))
payload = {'genesupin': len(tflist),'genesdownin':stat1, 'genesup':0 , 'genesdown':0}
r = requests.put('http://localhost:8000/api/v1/params/1/', data=payload)