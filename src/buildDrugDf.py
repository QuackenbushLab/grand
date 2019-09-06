import subprocess
import pandas as pd
import numpy as np
import os

#Read network dimension
os.chdir('/Users/mab8354/granddb/src')
dimNet = pd.read_csv('dimNet.csv')

# Initialize dataframe
df = pd.DataFrame(columns=['number','drug','tool','netzoo','network','ppi','motif','expression','tfs','genes','refs'])

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
numbersVec    = []
drugVec       = []
ppiVec        = []
refsVec       = []
missing=0
for line in res.splitlines():
    print(line)
    nDrugs = nDrugs + 1
    drug   = str(line.split()[-1]).split('.')[0][2:]
    drugList.append(drug)
    networkVec.append('<a href="' + 'https://granddb.s3.amazonaws.com/drugs/drugNetworks/' + drug + '.txt.mat' + '" download><i class="fas fa-download"></i></a>')
    expressionVec.append('<a href="' + 'https://granddb.s3.amazonaws.com/drugs/drugExpression/' + drug + '.txt' + '"><i class="fas fa-download"></i></a> <a href="#"><i class="fas fa-link"></i></a>')
    numbersVec.append(nDrugs)
    drugVec.append('<a href = "' + '#' + '" >' + drug + '</a>')
    refsVec.append('<a href="#"><i class="fas fa-book"></i></a>')
    matching = [s for s in range(len(dimNet.iloc[:,0])) if drug+'.txt.mat' == dimNet.iloc[s,0]]
    if matching != []:
        tfsVec.append(dimNet.iloc[matching,1].values[0])
        genesVec.append(dimNet.iloc[matching,2].values[0])
    else:
        tfsVec.append(0)
        genesVec.append(0)
        missing=missing+1 # 3 are missing



# build vectors
toolVec       = np.repeat('PANDA', nDrugs)
netzooVec     = np.repeat('netZooM', nDrugs)
netzooLinkVec = np.repeat('netZooM <a href="https://github.com/netZoo/netZooM/releases">0.1</a>', nDrugs)
ppiVec        = np.repeat('<a href="https://granddb.s3.amazonaws.com/drugs/drugs_ppi.txt"><i class="fas fa-download"></i></a> <a href="http://string90.embl.de/"><i class="fas fa-link"></i></a>', nDrugs)
motifVec      = np.repeat('<a href="https://granddb.s3.amazonaws.com/drugs/drugs_motif.txt"><i class="fas fa-download"></i></a>', nDrugs)
expLinkVec    = np.repeat('#', nDrugs)

# Populate df
df['number']    = numbersVec
df['drug']      = drugVec
df['tool']      = toolVec
df['netzoo']    = netzooLinkVec
df['network']   = networkVec
df['ppi']       = ppiVec
df['motif']     = motifVec
df['expression']= expressionVec
df['tfs']       = tfsVec
df['genes']     = genesVec
df['refs']      = refsVec

# save dataframe
os.chdir('/Users/mab8354/granddb')
df.to_csv('drugs.csv', index=False)