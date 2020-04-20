import boto3
import pandas as pd
import dask.dataframe as dd
from io import StringIO
import os

tissues=['Adipose_Subcutaneous_Tissue' ,'Adipose_Visceral_Tissue' ,'Adrenal_Gland_Tissue' ,'Artery_Aorta_Tissue'
            ,'Artery_Coronary_Tissue'
            ,'Artery_Tibial_Tissue' ,'Brain_Basal_Ganglia_Tissue' ,'Brain_Cerebellum_Tissue'
            ,'Brain_Other_Tissue','Breast_Tissue' ,'Colon_Sigmoid_Tissue' ,'Colon_Transverse_Tissue' ,'Esophagus_Mucosa_Tissue'
            ,'Esophagus_Muscularis_Tissue' ,'Gastroesophageal_Junction_Tissue'
            ,'Heart_Atrial_Appendage_Tissue' ,'Heart_Left_Ventricule_Tissue' ,'Intestine_Terminal_Ileum_Tissue'
            ,'Liver_Tissue' ,'Lung_Tissue' ,'Pancreas_Tissue' ,'Pituitary_Tissue','Skeletal_Muscle_Tissue'
            ,'Skin_Tissue' ,'Spleen_Tissue' ,'Stomach_Tissue' ,'Thyroid_Tissue'
            ,'Tibial_Nerve_Tissue' ,'Whole_Blood_Tissue']
tissuesCase=['Adipose_subcutaneous_tissue' ,'Adipose_visceral_tissue' ,'Adrenal_gland_tissue' ,'Artery_aorta_tissue'
            ,'Artery_coronary_tissue'
            ,'Artery_tibial_tissue' ,'Brain_basal_ganglia_tissue' ,'Brain_cerebellum_tissue'
            ,'Brain_other_tissue','Breast_tissue' ,'Colon_sigmoid_tissue' ,'Colon_transverse_tissue' ,'Esophagus_mucosa_tissue'
            ,'Esophagus_muscularis_tissue' ,'Gastroesophageal_junction_tissue'
            ,'Heart_atrial_appendage_tissue' ,'Heart_left_ventricule_tissue' ,'Intestine_terminal_ileum_tissue'
            ,'Liver_tissue' ,'Lung_tissue' ,'Pancreas_tissue' ,'Pituitary_tissue','Skeletal_muscle_tissue'
            ,'Skin_tissue' ,'Spleen_tissue' ,'Stomach_tissue' ,'Thyroid_tissue'
            ,'Tibial_nerve_tissue' ,'Whole_blood_tissue']
nSamples = [380,234,159,247,140,357,779,254,360,217,173,203,176,330,283,217,267,137,360,469,334,193,124,661,104,118,204,355,444]
k=0
for slug3 in tissues:
    if slug3 in ['Adipose_Subcutaneous_Tissue' ,'Adipose_Visceral_Tissue' ,'Adrenal_Gland_Tissue' ,'Artery_Aorta_Tissue'
                 ,'Artery_Coronary_Tissue',
                 'Artery_Tibial_Tissue' ,'Brain_Basal_Ganglia_Tissue' ,'Brain_Cerebellum_Tissue'
                 ,'Brain_Other_Tissue']:  # Adipose_Subcutaneous_AllSamples.csv
        pathToFile = '/diskb/' + slug3[:-7] + '_AllSamples.csv'
    elif slug3 in ['Breast_Tissue' ,'Colon_Sigmoid_Tissue' ,'Colon_Transverse_Tissue' ,'Esophagus_Mucosa_Tissue'
                   ,'Esophagus_Muscularis_Tissue' ,'Gastroesophageal_Junction_Tissue',
                   'Heart_Atrial_Appendage_Tissue' ,'Heart_Left_Ventricule_Tissue' ,'Intestine_Terminal_Ileum_Tissue'
                   ,'Liver_Tissue' ,'Lung_Tissue' ,'Pancrease_Tissue' ,'Pituitary_Tissue']:
        pathToFile = '/diskc/' + slug3[:-7] + '_AllSamples.csv'
    elif slug3 in ['Skeletal_Muscle_Tissue' ,'Skin_Tissue' ,'Spleen_Tissue' ,'Stomach_Tissue' ,'Thyroid_Tissue'
                   ,'Tibial_Nerve_Tissue' ,'Whole_Blood_Tissue']:
        pathToFile = '/diskd/' + slug3[:-7] + '_AllSamples.csv'
    for sampleid in range(1,nSamples[k]+1):
        df_train = dd.read_csv(pathToFile, usecols=[sampleid])
        df_train = df_train.compute()
        tfs   = pd.read_csv('src/tissue_tfs.csv' ,header=None)
        genes = pd.read_csv('src/tissue_genes.csv' ,header=None)
        tfs.columns   = ['' ,'']
        genes.columns = ['' ,'']
        sampleNet  = pd.DataFrame(index=tfs.iloc[1: ,1] ,columns=genes.iloc[: ,1]
                                 ,data=df_train.iloc[: ,0].values.reshape((644 ,30243)))
        fileName   = tissuesCase[k] + '_sample' + '_' + df_train.columns[0] + '.csv'
        bucket     = 'granddb' # already created on S3
        csv_buffer = StringIO()
        sampleNet.to_csv(csv_buffer)
        s3_resource = boto3.resource('s3')
        res =s3_resource.Object(bucket, 'tissues/networks/lioness/singleSample/' + fileName).put(Body=csv_buffer.getvalue())
        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            os.system('/usr/local/bin/aws s3api put-object-acl --bucket granddb --key tissues/networks/lioness/singleSample/' + fileName  + ' --acl public-read')
            resURL ='https://granddb.s3.amazonaws.com/tissues/networks/lioness/singleSample/' + fileName
            print(resURL)
        else:
            print('error')