import boto3
import pandas as pd
from io import StringIO
import os

generateSample=1
if generateSample==1:
    pathToFile='Drugs_TF_Targeting_AllSamples.csv'
    df_train = pd.read_csv(pathToFile)
    k=df_train.shape[1]
    for sampleid in range(1, k):
        sampleNet  = pd.DataFrame(data=df_train.iloc[: ,[0,sampleid]] )
        fileName   = 'TFtargeting_' + df_train.columns[sampleid] + '.csv'
        bucket     = 'granddb' # already created on S3
        csv_buffer = StringIO()
        sampleNet.to_csv(csv_buffer)
        s3_resource = boto3.resource('s3')
        res =s3_resource.Object(bucket, 'drugs/drugNetwork/PANDA/TFsig/' + fileName).put(Body=csv_buffer.getvalue())
        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            os.system('aws s3api put-object-acl --bucket granddb --key drugs/drugNetwork/PANDA/TFsig/' + fileName  + ' --acl public-read')
            resURL ='https://granddb.s3.amazonaws.com/drugs/drugNetwork/PANDA/TFsig/' + fileName
            print(resURL)
        else:
            print('error')
    os.system('rm ' + pathToFile)

generateSample=1
if generateSample==1:
    pathToFile='Drugs_Gene_Targeting_AllSamples.csv'
    df_train = pd.read_csv(pathToFile)
    k=df_train.shape[1]
    for sampleid in range(1, k):
        sampleNet  = pd.DataFrame(data=df_train.iloc[: ,[0,sampleid]] )
        fileName   = 'Genetargeting_' + df_train.columns[sampleid] + '.csv'
        bucket     = 'granddb' # already created on S3
        csv_buffer = StringIO()
        sampleNet.to_csv(csv_buffer)
        s3_resource = boto3.resource('s3')
        res =s3_resource.Object(bucket, 'drugs/drugNetwork/PANDA/genesig/' + fileName).put(Body=csv_buffer.getvalue())
        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            os.system('aws s3api put-object-acl --bucket granddb --key drugs/drugNetwork/PANDA/genesig/' + fileName  + ' --acl public-read')
            resURL ='https://granddb.s3.amazonaws.com/drugs/drugNetwork/PANDA/genesig/' + fileName
            print(resURL)
        else:
            print('error')
    os.system('rm ' + pathToFile)
