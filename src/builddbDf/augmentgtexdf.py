import numpy as np
import pandas as pd

os.chdir('/Users/mab8354/granddb/')
# first fix the empty vars
df = pd.read_csv('data/GTExSamples_Variables.csv')
df.fillna('-', inplace=True)
df.to_csv('data/GTExSamples_Variables.csv')

# then augment the df
df = pd.read_csv('data/GTExSamples_Variables.csv',index_col=1)
allvars= pd.read_csv('data/GTExSamples_AllVariables.txt',sep='\t',index_col=0)
intersample =  np.intersect1d(df.index, allvars.index)

# Add vars
df['SMTSTPTREF']='-'
df['SMTSTPTREF'].loc[intersample] = allvars.loc[intersample]['SMTSTPTREF'].values
df['SMGNSDTC']='-'
df['SMGNSDTC'].loc[intersample]   = allvars.loc[intersample]['SMGNSDTC'].values
df['SMMNCPB'] ='-'
df['SMMNCPB'].loc[intersample]    = allvars.loc[intersample]['SMMNCPB'].values

df.to_csv('data/GTExSamples_Variables.csv')