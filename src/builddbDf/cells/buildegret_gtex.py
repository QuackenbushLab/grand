import pandas as pd
import os
import numpy as np

os.chdir('/Users/mab8354/granddb/data')

# GTEx samples (ALL)
gtex_sex=pd.read_csv('GTExSamples_AllVariables.txt',sep='\t')
gtex=pd.read_csv('GTEx_v7_Annotations_SampleAttributesDS.txt',sep='\t')

# EGRET samples
egret=pd.read_csv('LCL_expression.csv')
samples = egret.columns[1:]
# replace hyphens
samples = [x.replace('.','-') for x in samples]

# find samples in df
aa = np.intersect1d(samples, gtex_sex['SampleID'], return_indices=True)
a = np.intersect1d(samples, gtex['SAMPID'], return_indices=True)
b = gtex.iloc[a[2],]
b.rename(columns = {'SAMPID':'SampleID'}, inplace = True)

# select relevant columns
sex_samples = gtex_sex.iloc[aa[2],[0,1,2,3,4,5,6,15,31,35]]

# merge two subdfs
outer_merged = pd.merge(b, sex_samples, how='outer')

# do clean names
cleannames = [x.replace('-','_') for x in outer_merged['SampleID']]
outer_merged['cleanname'] = cleannames

# save final df
outer_merged.to_csv('egret_gtex.csv', index=False)