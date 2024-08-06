import os
import pandas as pd
import boto3

session = boto3.Session( aws_access_key_id='', aws_secret_access_key='')

s3 = session.resource('s3')

my_bucket = s3.Bucket('jqlabusers')

for my_bucket_object in my_bucket.objects.filter(Prefix="esaha/LIGER/BONOBO_2023/networks/GSE19783_bonobo_coexpression/"):
    if my_bucket_object.key=='esaha/LIGER/BONOBO_2023/networks/GSE19783_bonobo_coexpression/':
        continue
    print(my_bucket_object.key)
    os.system('curl -O https://jqlabusers.s3.us-east-2.amazonaws.com/'+my_bucket_object.key)
    filename=os.path.basename(my_bucket_object.key)
    df=pd.read_csv('/home/ubuntu/'+filename,sep='\t')
    mirIndex=19504
    mirNames =df.columns[mirIndex:]
    geneNames=df.columns[:mirIndex]
    newdf = df.iloc[mirIndex:,:mirIndex]
    newdf.index = mirNames
    newdf.to_csv('/home/ubuntu/Downloads/newnets/'+'BRCA_mirna_'+filename[:-4]+'.csv')
    os.system('rm /home/ubuntu/'+filename)

#expression
expfile='~/Downloads/GSE19783_miRNA_mRNA_expression.txt'
dfexp=pd.read_csv(expfile,sep=' ')
dfexp.to_csv('~/Downloads/GSE19783_miRNA_mRNA_expression.csv')


# Thryoid
# remove redundant samples

df1=pd.read_csv('~/Downloads/GTEx_thyroid_allSex.txt',sep='\t')
df2=pd.read_csv('~/Downloads/GTEx_thyroid_phenotypes_GRAND.txt',sep=" ")

samples=df1.columns[1:]

newdf2=df2.loc[samples,]

newind=[]
for i in range(len(newdf2.index)):
    newind.append(str.split(newdf2.index[i],'.')[0])

newdf2.index = newind
newdf2.to_csv('~/granddb/static/data/GTEx_thyroid_phenotypes_GRAND_red.csv')


#reformat PAANDA from edges to matrix
session = boto3.Session( aws_access_key_id='', aws_secret_access_key='')

s3 = session.resource('s3')

my_bucket = s3.Bucket('jqlabusers')

for my_bucket_object in my_bucket.objects.filter(Prefix="esaha/LIGER/BONOBO_2023/networks/BonoboPanda_GTEx_thyroid/single_panda/"):
    if my_bucket_object.key=='esaha/LIGER/BONOBO_2023/networks/BonoboPanda_GTEx_thyroid/single_panda/':
        continue
    print(my_bucket_object.key)
    os.system('curl -O https://jqlabusers.s3.us-east-2.amazonaws.com/'+my_bucket_object.key)
    filename=os.path.basename(my_bucket_object.key)
    df2net=pd.read_csv('/home/ubuntu/'+filename,sep='\t')
    df2net = df2net.drop(['motif'], axis=1)
    unstacked_df2net = df2net.pivot_table(columns='gene',index = 'tf')
    unstacked_df2net.to_csv('/home/ubuntu/Downloads/newnets/'+'THCA_PANDA_BONOBO_'+filename[:-6]+'.csv')
    os.system('rm /home/ubuntu/'+filename)




