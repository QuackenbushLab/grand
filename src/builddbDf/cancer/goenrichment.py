import pandas as pd
import os
from scipy.stats import zscore
import requests
import json
import matplotlib.pyplot as plt
import mygene
import time
import numpy as np
mg = mygene.MyGeneInfo()

os.chdir('/Users/mab8354/Downloads/network')

df = pd.read_csv('panda_ACC.csv', index_col=0)
ntfs  = df.shape[0]
ngenes= df.shape[1]

# reconcile PRAD
prad=pd.read_csv('~/Downloads/panda_tcga_prad.csv', index_col=0)
prad_df = pd.DataFrame(np.zeros( (ntfs, ngenes) ) )
prad_df.index = df.index
prad_df.columns = df.columns
a = np.intersect1d(prad_df.columns, prad.columns, return_indices=True)
ind=-1
for tf in prad_df.index :
    ind=ind+1
    if np.in1d(tf, prad.index) == 1:
        prad_df.iloc[ind, a[1]] = prad.iloc[ind, a[2]]
    else:
        continue

#fill 0 by column average first
prad_df=prad_df.mask(prad_df==0).fillna(prad_df.mean(axis=0), axis=0)
row_means = df.replace(0, np.nan).mean(axis=1)
#fill 0 by row average second
df = df.replace(0, row_means)

prad_df.to_csv('~/Downloads/network/panda_PRAD.csv')



cancertypes=["ACC","BLCA","CHOL","DLBC","ESCA","HNSC","KICH","KIRC","KIRP","LAML","LGG","LUAD","LUSC","MESO","PCPG","READ","SARC","SKCM","STAD","THCA","THYM","UVM","PRAD"]
tftarmat   = pd.DataFrame(data=np.zeros( (ntfs,len(cancertypes) )), columns=cancertypes, index=df.index)
genetarmat = pd.DataFrame(data=np.zeros( (ngenes,len(cancertypes) )), columns=cancertypes, index=df.columns)

for cancer in cancertypes:
    df = pd.read_csv('panda_'+cancer+'.csv',index_col=0)
    tftar  = df.sum(axis=1)
    genetar= df.sum(axis=0)
    tftarmat[cancer] = tftar.values
    genetarmat[cancer] = genetar.values

# zscore matrices
tftarmat=tftarmat.transpose()
genetarmat=genetarmat.transpose()
tftarmat=tftarmat.apply(zscore)
genetarmat=genetarmat.apply(zscore)
tftarmat=tftarmat.transpose()
genetarmat=genetarmat.transpose()

# GO enrichemnt
processBio = pd.DataFrame(data=np.zeros((len(cancertypes)*10,4)) ,columns=['cell','term','go','logpval'])
j=-10
for net in tftarmat.columns:
    j=j+10
    print(net,j)
    time.sleep(5)
    c=tftarmat[np.abs(tftarmat[net]) > 1].index
    genes_str='\n'.join(c)
    ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/addList'
    query_string = '?userListId=%s&backgroundType=%s'

    description = 'Example gene list'
    payload = {
        'list': (None, genes_str),
        'description': (None, description)
    }

    response = requests.post(ENRICHR_URL, files=payload)
    if not response.ok:
        raise Exception('Error analyzing gene list')

    data = json.loads(response.text)
    user_list_id = data['userListId']
    gene_set_library = 'GO_Biological_Process_2018'
    ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/enrich'
    response = requests.get(
        ENRICHR_URL + query_string % (user_list_id, gene_set_library)
     )
    if not response.ok:
        raise Exception('Error fetching enrichment results')

    data = json.loads(response.text)
    for i in range(10):
        processBio['cell'].iloc[j+i] = net
        res=str.split(data['GO_Biological_Process_2018'][i][1], 'GO')
        processBio['go'].iloc[j+i] = res[0][0:-2]
        processBio['term'].iloc[j+i] = 'GO'+res[1][:-2]
        if data['GO_Biological_Process_2018'][i][2] == 0:
            processBio['logpval'].iloc[j + i] = 300
        else:
            processBio['logpval'].iloc[j+i] = -np.log10(data['GO_Biological_Process_2018'][i][2])


# GO enrichemnt
processBioGene = pd.DataFrame(data=np.zeros((len(cancertypes)*10,4)) ,columns=['cell','term','go','logpval'])
j=-10
for net in genetarmat.columns:
    j=j+10
    print(net)
    time.sleep(5)
    c=genetarmat[np.abs(genetarmat[net]) > 2].index
    geneSyms = mg.querymany(c, scopes=["ensemblgene", "symbol"], fields='symbol', species='human',
                            as_dataframe=True)
    #geneSyms=geneSyms[geneSyms.notfound != True]
    geneSyms =  geneSyms[np.logical_not( geneSyms['symbol'].isna() )]
    c=geneSyms.symbol.values
    genes_str='\n'.join(c)
    ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/addList'
    query_string = '?userListId=%s&backgroundType=%s'

    description = 'Example gene list'
    payload = {
        'list': (None, genes_str),
        'description': (None, description)
    }

    response = requests.post(ENRICHR_URL, files=payload)
    if not response.ok:
        raise Exception('Error analyzing gene list')

    data = json.loads(response.text)
    user_list_id = data['userListId']
    gene_set_library = 'GO_Biological_Process_2018'
    ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/enrich'
    response = requests.get(
        ENRICHR_URL + query_string % (user_list_id, gene_set_library)
     )
    if not response.ok:
        raise Exception('Error fetching enrichment results')

    data = json.loads(response.text)
    for i in range(10):
        res=str.split(data['GO_Biological_Process_2018'][i][1], 'GO')
        processBioGene['go'].iloc[j+i] = res[0][0:-2]
        processBioGene['term'].iloc[j+i] = 'GO'+res[1][:-2]
        processBioGene['cell'].iloc[j+i] = net
        if data['GO_Biological_Process_2018'][i][2] == 0:
            processBioGene['logpval'].iloc[j + i] = 300
        else:
            processBioGene['logpval'].iloc[j+i] = -np.log10(data['GO_Biological_Process_2018'][i][2])


# save dfs
processBioGene.index.name='index'
processBioGene.to_csv('/Users/mab8354/granddb/data/cancerbiogene.csv')
processBio.index.name='index'
processBio.to_csv('/Users/mab8354/granddb/data/cancerbio.csv')






#prad=pd.read_csv('~/Downloads/panda_tcga_prad.csv', index_col=0)
#df = pd.read_csv('~/Downloads/panda_ACC.csv', index_col=0)