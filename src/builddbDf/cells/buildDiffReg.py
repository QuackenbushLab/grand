import numpy as np
import pandas as pd
from scipy.stats import zscore
import os

os.chdir('/Users/mab8354/')

exprs    = pd.read_csv('netzoopap/data/CCLE_expression.csv',index_col=0)
exprs    = pd.read_csv('netzoopap/data/CCLE_expression.csv',index_col=0)
tftar    = pd.read_csv('netzoopap/data/CCLE_tftar.csv',index_col=0)
genetar    = pd.read_csv('netzoopap/data/CCLE_genetar.csv',index_col=0)
tftar=tftar.transpose()
genetar=genetar.transpose()
cellnet  = pd.read_csv('Downloads/ACH-000556.csv',index_col=0) # or any cell line

codingGeneNames = []
for i in range(len(exprs.columns)):
    codingGeneNames.append(str.split(exprs.columns[i], ' ')[0])
exprs.columns=codingGeneNames

# first z-score by gene (columns)
zexp    = exprs.apply(zscore)
tftar   = tftar.apply(zscore)
genetar = genetar.apply(zscore)

# fetch tf list names
tfs=cellnet.index

# filter tfs
intertfs = np.intersect1d(zexp.columns, tfs)
zexptfs = zexp.loc[:,intertfs]

# threshold z-score 2
bardata = np.sum(np.abs(zexptfs) > 2, axis=1)
bardatagenes=np.sum(np.abs(zexp) > 2, axis=1)


bardatatar     = np.sum(np.abs(tftar) > 2, axis=1)
bardatagenestar= np.sum(np.abs(genetar) > 2, axis=1)


