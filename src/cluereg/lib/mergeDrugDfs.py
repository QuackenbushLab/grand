import pandas as pd
import numpy as np

df1=pd.read_csv('/Users/mab8354/granddb/src/clueReg/data/drugNames.csv',header=None)
df2=pd.read_csv('/Users/mab8354/Downloads/GSE92742_Broad_LINCS_pert_info.txt',sep='\t')

b1, ib = np.unique(df2.iloc[:,1], return_index=True)

df2=df2.iloc[ib]

indInter=np.in1d(df2.iloc[:,1], df1.iloc[:,0])

a=np.where(indInter)

#indInter2=np.in1d(df1.iloc[:,0], df2.iloc[:,1])

#inds=np.where(indInter2 == False)

df2=df2.iloc[a]

indInter=np.in1d(df1.iloc[:,0], df2.iloc[:,1])

b=np.where(indInter)

df2.index = b

df =pd.concat([df1, df2], axis=1)

df.to_csv('/Users/mab8354/granddb/src/clueReg/data/drugNamesAug.csv')



