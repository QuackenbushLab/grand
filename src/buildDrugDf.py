import subprocess
import pandas as pd
import numpy as np

# Initialize dataframe
df = pd.DataFrame(columns=['drug','drugLink','tool','netzoo','netzooLink','netzooRel','network','ppi','ppiLink','motif','expression','expLink','tfs','genes','refs'])

# Read from bucket
batcmd="aws s3 ls s3://cmapreg/data/drugNetworks/"
res = subprocess.check_output(batcmd, shell=True)

# Loop through files
nDrugs = 0
drugList = []
genesVec = []
tfsVec   = []
expressionVec = []
networkVec    = []
for line in res.splitlines():
    print(line)
    nDrugs = nDrugs + 1
    drug   = str(line.split()[-1]).split('.')[0][2:]
    drugList.append(drug)
    networkVec.append('https://granddb.s3.amazonaws.com/drugs/drugNetworks/' + drug + '.txt.mat')
    expressionVec.append('https://granddb.s3.amazonaws.com/drugs/drugExpression/' + drug + '.txt')
    tfsVec.append(nDrugs)
    genesVec.append(nDrugs)

# build vectors
drugVec       = drugList
drugLinkVec   = np.repeat('#',nDrugs)
toolVec       = np.repeat('PANDA',nDrugs)
netzooVec     = np.repeat('netZooM',nDrugs)
netzooLinkVec = np.repeat('https://github.com/netZoo/netZooM/releases',nDrugs)
netzooRelVec  = np.repeat('0.1',nDrugs)
ppiVec        = np.repeat('https://granddb.s3.amazonaws.com/drugs/drugs_ppi.txt',nDrugs)
ppiLinkVec    = np.repeat('http://string90.embl.de/', nDrugs)
motifVec  = np.repeat('https://granddb.s3.amazonaws.com/drugs/drugs_motif.txt', nDrugs)
expLinkVec    = np.repeat('#', nDrugs)
refsVec       = np.repeat('#', nDrugs)

# Populate df
df['drug']      = drugVec
df['drugLink']  = drugLinkVec
df['tool']      = toolVec
df['netzooLink']= netzooLinkVec
df['netzooRel'] = netzooRelVec
df['network']   = networkVec
df['ppi']       = ppiVec
df['ppiLink']   = ppiLinkVec
df['motif']     = motifVec
df['expression']= expressionVec
df['expLink']   = expLinkVec
df['tfs']       = tfsVec
df['genes']     = genesVec
df['refs']      = refsVec

# save dataframe
os.chdir('/Users/mab8354/granddb')
df.to_csv('drugs.csv',index=False)