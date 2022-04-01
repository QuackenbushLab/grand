import os
import pandas as pd


os.chdir('/Users/mab8354/granddb')

df=pd.read_csv('data/GTEx_v7_Annotations_SampleAttributesDS.txt',sep='\t')

b=np.where([df['SMTSD'] == 'Cells - EBV-transformed lymphocytes'])