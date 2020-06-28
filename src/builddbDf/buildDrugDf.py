import subprocess
import pandas as pd
import numpy as np
import os

#Read network dimension
os.chdir('/Users/mab8354/granddb/')

#0. read drug list
dfd=pd.read_csv('drugs.csv')
drugs=dfd.drug.values
cid=dfd.cid.values
samples=dfd.samples.values

#1. landing page
# Initialize dataframe
df    = pd.DataFrame(columns=['number','drug','tool','netzoo','netzooRel','network','ppi','motif','expression','tfs','genes','refs',
                              'ppiLink','samples','expLink','nnets','druglink'])
# add samples, type of optPANDA netowrk or parameters

#Initialize variables
nDrugs = 0
drugList = []
genesVec = []
tfsVec   = []
expressionVec    = []
networkVec       = []
numbersVec       = []
drugVec          = []
ppiVec,motifVec  = [],[]
refsVec          = []
drugVecApi       = []
networkVecApi    = []
expressionVecApi = []
ppilinkVec       = []
refsVecApi       = []
toolVec,expLink  = [],[]
samplesVec,druglink = [],[]
missing=0
netTypes  =['PANDA'] #,'optPANDA (ChIP-seq)','optPANDA (TFKD)','optPANDA (FunBind)']
netFolder =['PANDA'] #,'chipSeq','tfKd','funBind']

# Loop through drugs
for drug in drugs:
    print(drug)
    if drug=='0\'':
        print(drug)
        continue
    for netl in range(len(netTypes)):
        networkVec.append('https://granddb.s3.amazonaws.com/drugs/drugNetwork/' + netFolder[netl] + '/' + drug + '.csv')
        expressionVec.append('https://granddb.s3.amazonaws.com/drugs/drugExpression/' + 'Drugs_Gene_Expression_AllSamples.csv')
        numbersVec.append(nDrugs)
        drugVec.append(drug)
        if cid[nDrugs] not in [0,-666]:
            ref2add=cid[nDrugs]
        else:
            ref2add = '#'
        refsVec.append('https://pubchem.ncbi.nlm.nih.gov/compound/' + ref2add)
        if netTypes[netl]=='PANDA':
            tfsVec.append(652)
            ppilinkVec.append('http://string90.embl.de/')
            motifVec.append('https://granddb.s3.amazonaws.com/optPANDA/motifs/Hugo_motifCellLine.txt')
        else:
            tfsVec.append(1603)
            ppilinkVec.append('https://string-db.org/')
            motifVec.append('https://granddb.s3.amazonaws.com/optPANDA/motifs/regMatPval1e3.csv')
        if netTypes[netl] == 'PANDA':
            ppiVec.append('https://granddb.s3.amazonaws.com/drugs/drugs_ppi.txt')
        elif netTypes[netl] == 'optPANDA (FunBind)':
            ppiVec.append('https://granddb.s3.amazonaws.com/optPANDA/ppi/ppi_complete.txt')
        elif netTypes[netl] == 'optPANDA (ChIP-seq)':
            ppiVec.append('https://granddb.s3.amazonaws.com/optPANDA/ppi/ppi_complete_bind.txt')
        elif netTypes[netl] == 'optPANDA (TFKD)':
            ppiVec.append('https://granddb.s3.amazonaws.com/optPANDA/ppi/2ppi_complete_bind.txt')
        genesVec.append(12328)
        toolVec.append(netTypes[netl])
        drugVecApi.append(drug)
        druglink.append('<a href="https://grand.networkmedicine.org/drugs/' + drug +'_drug">'+drug+'</a>')
        networkVecApi.append('https: /granddb.s3.amazonaws.com/drugs/drugNetwork/' + netFolder[netl] + '/' + drug + '.csv')
        samplesVec.append(samples[nDrugs])
        expressionVecApi.append('s3://granddb/drugs/drugExpression/' + drug + '.txt')
        nDrugs = nDrugs + 1

# build vectors
netzooLinkVec = np.repeat('netZooM', nDrugs)
refsVecApi    = np.repeat('#', nDrugs)

# Populate df
df['number']    = np.array(numbersVec)+1
df['drug']      = drugVec
df['tool']      = toolVec
df['netzoo']    = netzooLinkVec
df['network']   = networkVec
df['ppi']       = ppiVec
df['ppiLink']   = ppilinkVec
df['motif']     = motifVec
df['expression']= expressionVec
df['tfs']       = tfsVec
df['genes']     = genesVec
df['refs']      = refsVec
df['samples']   = samplesVec
df['netzooRel'] = ['0.4.3']*nDrugs
df['expLink']   = ['https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE92742']*nDrugs
df['nnets']     = np.ones((nDrugs), dtype = int)
df['druglink']  = druglink

# save dataframe
os.chdir('/Users/mab8354/granddb')
df.to_csv('drugslanding.csv', index=False)
