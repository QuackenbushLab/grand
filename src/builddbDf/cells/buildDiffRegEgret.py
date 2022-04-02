import numpy as np
import pandas as pd
from scipy.stats import zscore
import os
import boto3
from io import StringIO
import mygene

mg = mygene.MyGeneInfo()
os.chdir('/Users/mab8354/')

samples = pd.read_csv('granddb/data/banovich_YRI_genotype_info_for_grand.csv')

def normalizeFun(tftar,genetar):
    # first z-score by gene (columns)
    tftar = tftar.transpose()
    genetar = genetar.transpose()
    tftar = tftar.apply(zscore)
    genetar = genetar.apply(zscore)
    bardatatar = np.sum(np.abs(tftar) > 2, axis=1)
    bardatagenestar = np.sum(np.abs(genetar) > 2, axis=1)
    return bardatatar, bardatagenestar

# 1. For IPSC
ntfs     = 687
ngenes   = 9394
nsamples = 119
samplesnet = samples[samples['net'] == 'ipsc']
tftaripsc = pd.DataFrame(np.zeros((ntfs,119)))
genetaripsc = pd.DataFrame(np.zeros((ngenes,119)))
genetaripsc.columns = samplesnet['Sample.name']
tftaripsc.columns = samplesnet['Sample.name']
for name in samplesnet['Sample.name']:
    print(name)
    object_key = 'cells/networks/iPSC/EGRET_iPSC_'+name+'.csv'
    client = boto3.client('s3',
             aws_access_key_id="",# this is an old key
             aws_secret_access_key="")
    bucket_name = 'granddb'
    csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string),index_col=0,sep=',')
    genetarins = df.sum(axis=0)
    tftarins = df.sum(axis=1)
    tftaripsc[name] = tftarins.values
    genetaripsc[name] = genetarins.values
tftaripsc.index = df.index
# convert tf names
tfNamessym = df.index
resmg = mg.querymany(tfNamessym, scopes='symbol', fields = 'ensembl.gene',species='human', as_dataframe=True, returnall = 0)
tfNames = resmg['ensembl.gene'].dropna()
tfNames=tfNames.values
genetaripsc.index = df.columns
# zscore
[bardatatar,bardatagenestar]=normalizeFun(tftaripsc,genetaripsc)

# 2. For IPSC-CM
ntfs     = 687
ngenes   = 18855
nsamples = 119
samplesnet = samples[samples['net'] == 'cm']
tftarcm = pd.DataFrame(np.zeros((ntfs,119)))
genetarcm = pd.DataFrame(np.zeros((ngenes,119)))
genetarcm.columns = samplesnet['Sample.name']
tftarcm.columns = samplesnet['Sample.name']
for name in samplesnet['Sample.name']:
    print(name)
    object_key = 'cells/networks/CM/EGRET_CM_'+name+'.csv'
    client = boto3.client('s3',
             aws_access_key_id="AKIATSKOPZNVUURWA424",
             aws_secret_access_key="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")
    bucket_name = 'granddb'
    csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string),index_col=0,sep=',')
    genetarins = df.sum(axis=0)
    tftarins = df.sum(axis=1)
    tftarcm[name] = tftarins.values
    genetarcm[name] = genetarins.values
tftarcm.index = df.index
genetarcm.index = df.columns
# zscore
[bardatatarcm,bardatagenestarcm]=normalizeFun(tftarcm,genetarcm)

# 3. Expression
def diffExp(object_key):
    client = boto3.client('s3',
                          aws_access_key_id="AKIATSKOPZNVUURWA424",
                          aws_secret_access_key="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")
    bucket_name = 'granddb'
    csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
    body    = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    exprs   = pd.read_csv(StringIO(csv_string), index_col=0, sep=',')
    exprs = exprs.transpose()
    zexp    = exprs.apply(zscore)
    # fetch tf list names
    tfs=tfNames
    # filter tfs
    intertfs = np.intersect1d(zexp.columns, tfs)
    zexptfs = zexp.loc[:,intertfs]
    # zscore
    bardata = np.sum(np.abs(zexptfs) > 2, axis=1)
    bardatagenes=np.sum(np.abs(zexp) > 2, axis=1)
    return bardata, bardatagenes, exprs

object_key = 'cells/expression/banovich_iPSC_expression.csv'
[bardata, bardatagenes]=diffExp(object_key)
object_key = 'cells/expression/banovich_iPSC-CM_expression.csv'
[bardatacm, bardatagenescm]=diffExp(object_key)

# plug back in data

egretdf = pd.read_csv('granddb/data/banovich_YRI_genotype_info_for_grand.csv',index_col=0)
egretdf['diffexp']      = 0
egretdf['diffexpgenes'] = 0
egretdf['difftar']      = 0
egretdf['difftargenes'] = 0
egretdf['presexp'] = 0
# intersect cell index
egretdf.loc[bardata.index,'presexp'] = 1
# difftar
egretdf.loc[egretdf.net == 'ipsc', 'difftar'] = bardatatar.values
egretdf.loc[egretdf.net == 'cm', 'difftar']   = bardatatarcm.values
# difftar genes
egretdf.loc[egretdf.net == 'ipsc', 'difftargenes'] = bardatagenestar.values
egretdf.loc[egretdf.net == 'cm', 'difftargenes']   = bardatagenestarcm.values
# diff exp
egretdf.loc[np.in1d(egretdf.index, bardata.index) & (egretdf.net == 'ipsc'), 'diffexp'] = bardata.values
egretdf.loc[np.in1d(egretdf.index, bardatacm.index) & (egretdf.net == 'cm'), 'diffexp'] = bardatacm.values
# diffexp genes
egretdf.loc[np.in1d(egretdf.index, bardatagenes.index) & (egretdf.net == 'ipsc'), 'diffexpgenes'] = bardatagenes.values
egretdf.loc[np.in1d(egretdf.index, bardatagenescm.index) & (egretdf.net == 'cm'), 'diffexpgenes'] = bardatagenescm.values

# save dataframe
egretdf.to_csv('~/granddb/data/diffexp_banovich_YRI_genotype_info_for_grand.csv')
