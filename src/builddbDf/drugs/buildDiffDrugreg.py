import numpy as np
import pandas as pd
from scipy.stats import zscore
import os

exprs    = pd.read_csv('Drugs_Gene_Expression_AllSamples.csv',index_col=0)
tftar    = pd.read_csv('Drugs_TF_Targeting_AllSamples.csv',index_col=0)
genetar  = pd.read_csv('Drugs_Gene_Targeting_AllSamples.csv',index_col=0)
tftar=tftar.transpose()
genetar  = genetar.transpose()
exprs = exprs.tranpose()
cellnet  = pd.read_csv('TFtargeting_CPC018_A375_6H:BRD-K06817181-001-01-5:10.csv',index_col=1) # or any cell line

# load sample data
sampledata=pd.read_csv('drug_vars_difftar_genetar.csv',index_col=0)

# first z-score by gene (columns)
#zexp    = exprs.apply(zscore) # no need to zscore since they zscores already
tftar   = tftar.apply(zscore)
genetar = genetar.apply(zscore)

# fetch tf list names
tfs=cellnet.index

# filter tfs
intertfs = np.intersect1d(zexp.columns, tfs)
zexptfs = exprs.loc[:,intertfs]

# threshold z-score 2 expression
bardata     = np.sum(np.abs(zexptfs) > 2, axis=1)
bardatagenes= np.sum(np.abs(zexp) > 2, axis=1)

# targeting
bardatatar     = np.sum(np.abs(tftar) > 2, axis=1)
bardatagenestar= np.sum(np.abs(genetar) > 2, axis=1)

# update drug vars
sampledata['difftar'] = 0
sampledata['difftar'].loc[bardatatar.index] = bardatatar.loc[bardatatar.index]

sampledata['difftargenes'] = 0
sampledata['difftargenes'].loc[bardatagenestar.index] = bardatagenestar.loc[bardatagenestar.index]

sampledata['diffexp'] = 0
sampledata['diffexp'].loc[bardata.index] = bardata.loc[bardata.index]


sampledata['diffexpgenes'] = 0
sampledata['diffexpgenes'].loc[bardatagenes.index] = bardatagenes.loc[bardatagenes.index]

# save
sampledata.to_csv('drug_vars_difftar_genetar_tfexp_geneexp.csv',index=True)
sampledata = pd.read_csv('/Users/mab8354/granddb/data/drug_vars_difftar_genetar_tfexp_geneexp.csv',index_col=0)

# II. compute nsamples per drug
os.chdir('/Users/mab8354/granddb/data')
df=pd.read_csv('drugslanding.csv',index_col=1)
df2=pd.read_csv('drug_vars_difftar_genetar_tfexp_geneexp.csv',index_col=1)
df['nsamples']  = 0
df['avgtftar']  = 0
df['avggenetar']= 0

for drug in df.index:
    df['nsamples'].loc[drug] = np.sum(df2.index==drug)-1 # remove All
    df['avgtftar'].loc[drug] = np.round(np.mean(df2[df2.index==drug]['difftar']),4)
    df['avggenetar'].loc[drug] = np.round(np.mean(df2[df2.index==drug]['difftargenes']),4)

df.to_csv('drugslanding.csv',index=True)

# clean names
sampledata=pd.read_csv('drug_vars_difftar_genetar_tfexp_geneexp.csv',index_col=0)
sampledata['cleannames'] = ''
cleannames=[]
for i in sampledata.index:
    if i!='-':
        i=str.replace(i,'-','_')
        i=str.replace(i,'.','_')
        i=str.replace(i,':','_')
        cleannames.append('drug_'+i)
    else:
        cleannames.append(i)


sampledata['cleannames'] = cleannames
#save df
sampledata.to_csv('drug_vars_difftar_genetar_tfexp_geneexp_clean.csv',index=True)

