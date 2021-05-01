import pandas as pd
import os

os.chdir('/Users/mab8354/granddb/')


df=pd.read_csv('data/GTExSamples_Variables.csv')
newNames=[]
for name in df['SampleID']:
    newNames.append(name.replace('-','_'))

df['cleanname'] = newNames
df.to_csv('data/GTExSamples_Variables_aug.csv')



