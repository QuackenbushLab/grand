import pandas as pd
import os
import numpy as np
from netZooPy import dragon

def Scale(X): #(temporaily)
    X_temp = X
    X_std = np.std(X_temp, axis=0)
    X_mean = np.mean(X_temp, axis=0)
    return (X_temp - X_mean) / X_std


def createVisNet(methyl,expression,r_methyl_mrna,methylMat,layer1,layer2,nedges=2000):
    if methyl.shape[1]==expression.shape[0]:
        pdNames_methyl_mrna = methyl.index.append(expression.columns)
    elif methyl.shape[0]==expression.shape[1]: #>>> methyl.shape (255, 19138) >>> expression.shape (12755, 255)
        pdNames_methyl_mrna = methyl.columns.append(expression.index)
    elif methyl.shape[0] == expression.shape[0]:
        pdNames_methyl_mrna = methyl.columns.append(expression.columns)
    r_methyl_mrna_pd = pd.DataFrame(r_methyl_mrna,index=pdNames_methyl_mrna,columns=pdNames_methyl_mrna)
    r_methyl_mrna_pd = r_methyl_mrna_pd.iloc[:methylMat.shape[1],methylMat.shape[1]:]
    return r_methyl_mrna_pd

os.chdir('/Users/mab8354/netzoopap/')

# Parameters
imputationMissing='zero'

# 0. Load metadata
cellNames=pd.read_csv('data/sample_info.csv')

# II. MiRna-mRNA
# 1. Read miRNA and mRNA
mirna=pd.read_csv('data/CCLE_miRNA_20181103.gct',sep='\t',comment='#',skiprows=2,index_col=1)
expression=pd.read_csv('data/CCLE_expression.csv',index_col=0)
# 2. remove unnecessary columns
mirna = mirna.iloc[:,1:]
# 3. convert cell names to depmap IDs # fetch these functions from dragonNet.py
mirna=convertToDepMap(mirna,cellNames)
# 4. align dataframes
expression,mirna=alignDF(expression,mirna,remove_std=1)
# 5. Call DRAGON
mirnaMat     = mirna.values
expressionMat= expression.values
# 6. Transpose and scale arrays (do not transpose expression)
mirnaMat     = Scale(np.transpose(mirnaMat)) #replace by dragon.scale
expressionMat= Scale(expressionMat)
# 7. Estimate lambdas
r_mir_exp, adj_p_vals_mir_exp=estimateDragonValues(mirnaMat, expressionMat)
# 8. take mirna to mRNA network
mir_exp_edges=createVisNet(mirna,expression,r_mir_exp,mirnaMat,'mir','exp')

# clean up genes names
mirnanet = pd.read_csv('~/Downloads/dragon_mirna_CCLE.csv', index_col=0)

mirVec=[]
for mir in mirnanet.columns:
    mirVec.append(str.split(mir,' ')[0])

mirnanet.columns = mirVec

mirnanet.to_csv('~/Downloads/dragon_mirna_CCLE.csv')





# build merged gene and mirna expression
mirna = pd.read_csv('data/CCLE_miRNA_20181103.gct', sep='\t', comment='#', skiprows=2, index_col=1)
mirna = mirna.iloc[:, 1:]
expression = pd.read_csv('data/CCLE_expression.csv', index_col=0)

newvec=[]
for exp in expression.columns:
    newvec.append(str.split(exp,' ')[0])
expression.columns = newvec

mirna=convertToDepMap(mirna,cellNames)
# 4. align dataframes
expression,mirna=alignDF(expression,mirna,remove_std=1)
mirna=mirna.transpose()
a=pd.concat((expression, mirna) ,axis=1)
a.to_csv('~/Downloads/merged_gene_mirna.csv')




