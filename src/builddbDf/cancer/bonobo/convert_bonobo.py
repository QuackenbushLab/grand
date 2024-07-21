import pandas as pd

filename='bonobo_GSM496794'
df=pd.read_csv('~/Downloads/'+filename+'.txt',sep='\t')

mirIndex=19504
mirNames =df.columns[mirIndex:]
geneNames=df.columns[:mirIndex]

newdf = df.iloc[mirIndex:,:mirIndex]
newdf.index = mirNames

newdf.to_csv('~/Downloads/'+'BRCA_mirna_'+filename+'.csv')

#expression
expfile='~/Downloads/GSE19783_miRNA_mRNA_expression.txt'
dfexp=pd.read_csv(expfile,sep=' ')
dfexp.to_csv('~/Downloads/GSE19783_miRNA_mRNA_expression.csv')