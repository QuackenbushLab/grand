import pandas as pd
import os

os.chdir('/Users/mab8354/granddb/data')
df=pd.read_csv('cancer.csv')

# build nTFs and ngenes

os.chdir('/Users/mab8354/Downloads')

for i in range(9,len(df)):
    tissue=df['tcgacode'].iloc[i]
    df2=pd.read_csv('expression/expression_tcga_'+tissue+'.txt', sep='\t')
    df['nsamples'].iloc[i]=df2.shape[1]

os.chdir('/Users/mab8354/granddb/data')
df.to_csv('cancer_aug.csv',index=False)


# build phenotypic information page
cancer='ACC'
dfpheno = pd.read_csv('~/Downloads/phenotypic/pheno_tcga_' + cancer + '.txt', sep='\t')
for cancer in ["BLCA","CHOL","COAD","DLBC","ESCA","GBM","HNSC","KICH","KIRC","KIRP","LAML","LGG","LIHC","LUAD","LUSC","MESO","PAAD","PCPG","READ","SARC","SKCM","STAD","THCA","THYM","UVM"]:
    dfpheno2 = pd.read_csv('~/Downloads/phenotypic/pheno_tcga_' + cancer + '.txt', sep='\t')
    dfpheno=pd.concat([dfpheno,dfpheno2])

dfpheno.replace(np.nan,'-',inplace=True)
dfpheno.index.name='sample'
dfpheno.to_csv('/Users/mab8354/granddb/data/cancerpheno.csv')


