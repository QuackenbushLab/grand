import pandas as pd
import os
import numpy as np

os.chdir('/Users/mab8354/granddb/')
db1 = pd.read_csv('tissues.csv')

os.chdir('/Users/mab8354/granddb/src/diseaseEnr')
db  = pd.read_csv('TF-tissue-expression-pre.csv')
db2 = pd.read_csv('TF-tissue-target.csv')
res = pd.DataFrame(columns=['Tissues','TFs','Cond'])
res['Tissues'] = db1['tissue']
res['TFs']     = res['TFs'].astype(object)
nTissues       = len(res)
res['Cond']    = np.zeros(nTissues)

k=0
lenVec = []
for tissue in res['Tissues']:
    j=0
    res['TFs'].iloc[k]=[]
    for tissueCol in db['Tissues']:
        if tissue in tissueCol:
            print(tissue)
            res['TFs'].iloc[k].append(db.iloc[j,1])
        j=j+1
    lenVec.append(len(res['TFs'].iloc[k]))
    res['TFs'].iloc[k] = ','.join(res.iloc[k,1])
    k=k+1

res['Cond'] = lenVec
#save dataframe
res.to_csv('TF-tissue-expression.csv')

#Save Django model temaplte
os.chdir('/Users/mab8354/granddb/')
res2 = pd.DataFrame(columns=['id','tissue','count','intersect','pval','qval','query'])
res2.iloc[:,0] = list(range(1,nTissues+1))
res2.iloc[:,1] = res['Tissues']
res2.iloc[:,2] = lenVec
res2.iloc[:,3] = np.zeros(nTissues, dtype=int)
res2.iloc[:,4] = np.zeros(nTissues, dtype=int)
res2.iloc[:,5] = np.zeros(nTissues, dtype=int)
res2.iloc[:,6] = np.ones(nTissues, dtype=int)

#save dataframe
res2.to_csv('tissue-expression.csv',index=False)

#TF targeting tissues
res3 = res2
res3['count'] = db2['#TFsDifferentiallyTargetingSelectedCategories']
res3.to_csv('tissue-target.csv',index=False)