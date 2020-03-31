import subprocess
import pandas as pd
import numpy as np
import os

#Read network dimension
os.chdir('/Users/mab8354/granddb/')
samplesNet = pd.read_csv('drugSamples.csv')

#1. drugs page
nDrugs=0
numbersVec    = []
drugVec       = []
df    = pd.DataFrame(columns=['number','drug','nnets'])
batcmd = "aws s3 ls s3://granddb/drugs/drugNetwork/chipSeq/"
res = subprocess.check_output(batcmd, shell=True)
for line in res.splitlines():
    drug   = str(line.split()[-1]).split('.')[0][2:]
    if drug=='0\'':
        print(drug)
        continue
    nDrugs = nDrugs + 1
    numbersVec.append(nDrugs)
    drugVec.append('<a href = "' + drug + '-drug' + '" >' + drug + '</a>')

nnetsVec      = [4] * nDrugs
df['number'] = numbersVec
df['drug']   = drugVec
df['nnets']  = nnetsVec
os.chdir('/Users/mab8354/granddb')
df.to_csv('drugs.csv', index=False)

#2. landing page
# Initialize dataframe
df    = pd.DataFrame(columns=['number','drug','tool','netzoo','netzooRel','network','ppi','motif','expression','tfs','genes','refs','ppiLink','samples','expLink'])
# add samples, type of optPANDA netowrk or parameters

# Read from bucket
res = subprocess.check_output(batcmd, shell=True)

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
samplesVec       = []
missing=0
netTypes  =['PANDA','optPANDA (ChIP-seq)','optPANDA (TFKD)','optPANDA (FunBind)']
netFolder =['PANDA','chipSeq','tfKd','funBind']
funcStr = lambda s: s[:1].lower() + s[1:] if s else ''
# Loop through files
for line in res.splitlines():
    print(line)
    drug   = str(line.split()[-1]).split('.')[0][2:]
    if drug=='0\'':
        print(drug)
        continue
    for netl in range(len(netTypes)):
        nDrugs = nDrugs + 1
        networkVec.append('https://granddb.s3.amazonaws.com/drugs/drugNetwork/' + netFolder[netl] + '/' + drug + '.csv')
        expressionVec.append('https://granddb.s3.amazonaws.com/drugs/drugExpression/' + funcStr(drug) + '.txt')
        numbersVec.append(nDrugs)
        drugVec.append(drug)
        if samplesNet['cid'].loc[samplesNet['Var1']==funcStr(drug)].values[0] not in [0,-666]:
            ref2add=str(samplesNet['cid'].loc[samplesNet['Var1']==funcStr(drug)].values[0])
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
        if netTypes[netl] in ['PANDA','optPANDA (FunBind)']:
            ppiVec.append('https://granddb.s3.amazonaws.com/optPANDA/ppi/ppi_complete.txt')
        elif netTypes[netl] == 'optPANDA (ChIP-seq)':
            ppiVec.append('https://granddb.s3.amazonaws.com/optPANDA/ppi/ppi_complete_bind.txt')
        elif netTypes[netl] == 'optPANDA (TFKD)':
            ppiVec.append('https://granddb.s3.amazonaws.com/optPANDA/ppi/2ppi_complete_bind.txt')
        genesVec.append(12329)
        toolVec.append(netTypes[netl])
        drugVecApi.append(drug)
        networkVecApi.append('https: // granddb.s3.amazonaws.com/drugs/drugNetwork/' + netFolder[netl] + '/' + drug + '.csv')
        samplesVec.append(samplesNet['nSamples'].loc[samplesNet['Var1']==funcStr(drug)].values[0])
        expressionVecApi.append('s3://granddb/drugs/drugExpression/' + drug + '.txt')

# build vectors
netzooLinkVec = np.repeat('netZooM', nDrugs)
refsVecApi    = np.repeat('#', nDrugs)

# Populate df
df['number']    = numbersVec
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
df['netzooRel'] = ['0.4.2']*nDrugs
df['expLink']   = ['https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE92742']*nDrugs

# save dataframe
os.chdir('/Users/mab8354/granddb')
df.to_csv('drugslanding.csv', index=False)

# save APi dataframe
dfApi = df
dfApi['tool']          = toolVec
dfApi['netzoo']        = np.repeat('netZooM 0.4.2', nDrugs*4)
dfApi['ppi']           = np.repeat('s3://granddb/drugs//drugs_ppi.txt', nDrugs*4)
dfApi['motif']         = np.repeat('s3://granddb/drugs/drugs_motif.txt', nDrugs*4)
dfApi['drug']          = drugVecApi*4
dfApi['network']       = networkVecApi*4
dfApi['expression']    = expressionVecApi*4
dfApi['refs']          = refsVecApi

dfApi.to_csv('drugslandingApi.csv', index=False)
