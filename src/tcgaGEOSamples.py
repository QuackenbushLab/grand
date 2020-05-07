import pandas as pd
import os
from io import StringIO
import boto3
import numpy as np

geotcga=pd.read_csv('Colon_cancer_TCGA_AllSamples.txt',sep='\t')

for i in range(3,geotcga.shape[1]):
    sampleNet = pd.DataFrame(index=geotcga.iloc[0:661,0], columns=np.unique(geotcga.iloc[:,1])
                         , data=geotcga.iloc[:, i].values.reshape((12817, 661)).T)
    fileName = 'Colon_cancer_sample_' + geotcga.columns[i] + '.csv'
    bucket = 'granddb'  # already created on S3
    csv_buffer = StringIO()
    sampleNet.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    res = s3_resource.Object(bucket, 'cancer/colon_cancer/networks/lioness/' + fileName).put(Body=csv_buffer.getvalue())
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        os.system(
            'aws s3api put-object-acl --bucket granddb --key cancer/colon_cancer/networks/lioness/' + fileName + ' --acl public-read')
        resURL = 'https://granddb.s3.amazonaws.com/cancer/colon_cancer/networks/lioness/' + fileName
        print(resURL)
    else:
        print('error')

geotcga=pd.read_csv('Colon_cancer_GEO_AllSamples.txt',sep='\t')

for i in range(3,geotcga.shape[1]):
    sampleNet = pd.DataFrame(index=geotcga.iloc[0:661,0], columns=np.unique(geotcga.iloc[:,1])
                         , data=geotcga.iloc[:, i].values.reshape((12817, 661)).T)
    fileName = 'Colon_cancer_sample_' + geotcga.columns[i] + '.csv'
    bucket = 'granddb'  # already created on S3
    csv_buffer = StringIO()
    sampleNet.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    res = s3_resource.Object(bucket, 'cancer/colon_cancer/networks/lioness/' + fileName).put(Body=csv_buffer.getvalue())
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        os.system(
            'aws s3api put-object-acl --bucket granddb --key cancer/colon_cancer/networks/lioness/' + fileName + ' --acl public-read')
        resURL = 'https://granddb.s3.amazonaws.com/cancer/colon_cancer/networks/lioness/' + fileName
        print(resURL)
    else:
        print('error')

gg=geotcga.iloc[:,4:]
gg.to_csv('Colon_cancer_GEO_AllSamples.csv',sep=',')



