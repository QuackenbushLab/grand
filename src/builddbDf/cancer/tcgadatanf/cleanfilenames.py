import os
import pandas as pd
import boto3
from io import StringIO # python3; python2: BytesIO
import numpy as np

renamefiles=0
os.chdir('/Users/mab8354/Downloads')
client = boto3.client('s3',aws_access_key_id='', aws_secret_access_key='')
session = boto3.Session( aws_access_key_id='', aws_secret_access_key='')
s3 = session.resource('s3')

my_bucket = s3.Bucket('granddb')

cancers=['cancer/lung_cancer/lioness_tcga_luad/','cancer/colon_cancer/lioness_tcga_coad/','cancer/breast_cancer/lioness_tcga_brca/','cancer/lungsquamous_cancer/lioness_tcga_lusc/',
'cancer/kidney_cancer/lioness_tcga_kirc/','cancer/liver_cancer/lioness_tcga_lihc/','cancer/pancreas_cancer/lioness_tcga_paad/','cancer/prostate_cancer/lioness_tcga_prad/','cancer/skin_cancer/lioness_tcga_skcm/',
'cancer/stomach_cancer/lioness_tcga_stad/']


# 1. rename filesCreate DataFrame

networks,tids=[],[]
for cancer in cancers:
    print(cancer)
    i=0
    for my_bucket_object in my_bucket.objects.filter(Prefix=cancer):
        filename=os.path.basename(my_bucket_object.key)
        tids.append(cancer[-5:-1].upper())
        networks.append(my_bucket_object.key.split('/')[-1])
        i+=1

#
data = {'tumorID': tids,
        'net': networks}
tcganfdf = pd.DataFrame(data)

if renamefiles==1:
    for cancer in cancers:
        print(cancer)
        for my_bucket_object in my_bucket.objects.filter(Prefix=cancer):
            filename=os.path.basename(my_bucket_object.key)
            newfile="-".join(filename.split('.')[:-1])+".h5"
            copy_source = {'Bucket': 'granddb', 'Key': my_bucket_object.key}
            try:
                client.copy_object(Bucket='granddb', CopySource=copy_source,
                                   Key=cancer+newfile)
                client.delete_object(Bucket='granddb', Key=my_bucket_object.key)
            except:
                print(my_bucket_object.key)
                continue


# Add link and size for df
# part 1. 7/10 cancers
df=pd.read_csv('~/granddb/data/cancerpheno.csv')

#np.in1d(luad_df.columns, df.columns) # age_at_diagnosis is age at initial diagnosis
                                  # last_contact_days_to is days to last followup

tumorIDs = ['LUAD','LUSC','KIRC','PRAD','SKCM','STAD']
sizes = ['85.5 MB','86.1 MB','82.5 MB','81.7 MB','81.5 MB','83.9 MB']
tissues = ['lung','lungsquamous','kidney','prostate','skin','stomach']

i=0
cancernew = df.copy()
cancernew['ss'] = 0
for tumorID in tumorIDs:
    print(tumorID)
    luad_df = pd.read_csv('~/Downloads/clinical_patient_'+ tumorID.lower() +'.csv')
    # Add link and size to existing samples
    dc = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24], cancernew[cancernew['tumorID'] == tumorID]['sample'], return_indices=True)
    # intersect with tumor type
    #zz=np.intersect1d(np.where([tcganfdf['tumorID'] == tumorID]), dc[1])
    #ll=np.intersect1d(np.where([cancernew['tumorID'] == tumorID]), dc[2])
    linkstrant = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + \
                 '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[dc[1]]
    orig_ind = cancernew[cancernew['tumorID'] == tumorID]['sample'].index[dc[2]]
    cancernew['size'].iloc[orig_ind] = [sizes[i]]*len(orig_ind)
    cancernew['link'].iloc[orig_ind] = linkstrant.values
    cancernew['ss'].iloc[orig_ind] = 1
    # Add missing samples
    a=np.setdiff1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24], df['sample'][df['tumorID'] == tumorID])
    print(len(a))
    c=np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24].values, a, return_indices=True)
    b=np.intersect1d([aa[:-4] for aa in a], luad_df.bcr_patient_barcode.values, return_indices=True)
    linkstr = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[c[1]]
    if len(b[0]) == len(a):
        print('All good')
    dataadd = {'sample': a,
            'gender': luad_df.gender.iloc[b[2]].values,
            'race': luad_df.race.iloc[b[2]].values}
    if tumorID == 'PRAD':
        dataadd['ajcc_pathologic_tumor_stage'] = luad_df.clinical_stage.iloc[b[2]].values
    else:
        dataadd['ajcc_pathologic_tumor_stage'] = luad_df.ajcc_pathologic_tumor_stage.iloc[b[2]].values
    dataadd['vital_status'] = luad_df.vital_status.iloc[b[2]].values
    if tumorID == 'SKCM':
        dataadd['age_at_initial_pathologic_diagnosis'] = luad_df.age_at_diagnosis.iloc[b[2]].values
    else:
        dataadd['age_at_initial_pathologic_diagnosis'] = luad_df.age_at_initial_pathologic_diagnosis.iloc[b[2]].values
    dataadd['days_to_last_followup'] = luad_df.last_contact_days_to.iloc[b[2]].values
    dataadd['tumorID'] = [tumorID]*len(a)
    dataadd['link'] = linkstr
    dataadd['size'] = [sizes[i]]*len(a)
    dataadd['ss'] = 1
    concatdf  = pd.DataFrame(dataadd)
    cancernew = pd.concat((cancernew , concatdf))
    i=i+1

# add clean name
cancernew['submitter_id_clean'] = cancernew['tumorID']+'_'+ cancernew['link'].str.split('/').str[-1].str[:-3].str.replace('-','_')
# part 2
cancernew.to_csv('~/granddb/data/cancerpheno_extended.csv', index=False)

# Now Otter
# LIHC + BRCA
tumorIDs = ['LIHC','BRCA']
sizes = ['75.6 MB','84.0 MB']
tissues = ['liver','breast']
suppfile = ['_0123','_0129']

i=0
for tumorID in tumorIDs:
    print(tumorID)
    df = pd.read_csv('~/granddb/static/data/metadata_'+tissues[i]+suppfile[i]+'2021.csv')
    cancernew = df.copy()
    cancernew['ss'] = 0
    cancernew['size'] = 0
    cancernew['link'] = '-'
    luad_df = pd.read_csv('~/Downloads/clinical_patient_' + tumorID.lower() + '.csv')
    # Add link and size to existing samples
    dc = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24],
                        cancernew['gdc_cases.samples.portions.analytes.aliquots.submitter_id'].str[:16], return_indices=True)
    linkstrant = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + \
                 '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[dc[1]]
    orig_ind = cancernew['gdc_cases.samples.portions.analytes.aliquots.submitter_id'].index[dc[2]]
    cancernew['size'].iloc[orig_ind] = [sizes[i]] * len(orig_ind)
    cancernew['link'].iloc[orig_ind] = linkstrant.values
    cancernew['ss'].iloc[orig_ind] = 1
    # Add missing samples
    a = np.setdiff1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24], df['gdc_cases.samples.portions.analytes.aliquots.submitter_id'].str[:16])
    print(len(a))
    b = np.intersect1d([aa[:-4] for aa in a], luad_df.bcr_patient_barcode.values, return_indices=True)
    noclinical = np.setdiff1d(range(len(a)), b[1])
    #a = np.setdiff1d(a, a[noclinical])
    #c = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24].values, b[0], return_indices=True)
    if noclinical.size ==0:
        c = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24].values, a, return_indices=True)
    elif noclinical.size >0:
        c = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:20].values, b[0], return_indices=True)
    linkstr = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[c[1]]
    if len(b[0]) == len(a):
        print('All good')
    dataadd = {'gdc_cases.samples.portions.analytes.aliquots.submitter_id': a[b[1]],
    'gdc_cases.demographic.gender': luad_df.gender.iloc[b[2]].values,
    'gdc_cases.demographic.race': luad_df.race.iloc[b[2]].values}
    dataadd['gdc_cases.demographic.ethnicity'] = luad_df.ethnicity.iloc[b[2]].values
    if tumorID == 'LIHC':
        dataadd['gdc_cases.exposures.weight'] = luad_df.weight_kg_at_diagnosis.iloc[b[2]].values
        dataadd['gdc_cases.exposures.height'] = luad_df.height_cm_at_diagnosis.iloc[b[2]].values
        dataadd['gdc_cases.diagnoses.primary_diagnosis'] = luad_df.histologic_diagnosis.iloc[b[2]].values
    elif tumorID == 'BRCA':
        dataadd['gdc_cases.exposures.weight'] = 'NA'
        dataadd['gdc_cases.exposures.height'] = 'NA'
        dataadd['gdc_cases.diagnoses.primary_diagnosis'] = luad_df.histologic_diagnosis_other.iloc[b[2]].values
    dataadd['gdc_cases.project.primary_site'] = luad_df.tumor_tissue_site.iloc[b[2]].values
    dataadd['cgc_case_age_at_diagnosis'] = luad_df.age_at_diagnosis.iloc[b[2]].values
    dataadd['gdc_cases.diagnoses.tumor_stage'] = luad_df.ajcc_pathologic_tumor_stage.iloc[b[2]].values
    dataadd['gdc_cases.diagnoses.days_to_death'] = luad_df.death_days_to.iloc[b[2]].values
    dataadd['gdc_cases.diagnoses.vital_status'] = luad_df.vital_status.iloc[b[2]].values
    dataadd['link'] = linkstr
    dataadd['size'] = [sizes[i]] * len(b[0])
    dataadd['ss'] = [1] * len(b[0])
    concatdf = pd.DataFrame(dataadd)
    if noclinical.size >0: # put back the missing sample
        toadd = ['NA'] * (concatdf.shape[1])
        toadd[0] = a[noclinical][0]
        toadd[-1] = 1
        toadd[-2] = sizes[i]
        cc = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24].values, a[noclinical], return_indices=True)
        stradd = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[cc[1]]
        toadd[-3] = stradd.iloc[0]
        concatdf.loc[-1] = toadd
    cancernew = pd.concat((cancernew, concatdf))
    # add clean name
    cancernew['submitter_id_clean'] = tumorID + '_' + cancernew['link'].str.split('/').str[-1].str[:-3].str.replace('-', '_')
    cancernew.fillna('NA')
    # part 2
    cancernew.to_csv('~/granddb/static/data/metadata_'+tissues[i]+suppfile[i]+'2021_bis.csv', index=False)
    i = i + 1


# Now PAAD
tumorIDs = ['PAAD']
sizes = ['83.4 MB']
tissues = ['pancreas']

i=0
for tumorID in tumorIDs:
    print(tumorID)
    df = pd.read_csv('~/granddb/static/data/pancreas_tcga.csv')
    cancernew = df.copy()
    cancernew['ss'] = 0
    cancernew['size2'] = 0
    cancernew['link2'] = '-'
    luad_df = pd.read_csv('~/Downloads/clinical_patient_' + tumorID.lower() + '.csv')
    # Add link and size to existing samples
    dc = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24],
                        cancernew['gdc_cases.samples.portions.analytes.aliquots.submitter_id'].str[:16], return_indices=True)
    linkstrant = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + \
                 '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[dc[1]]
    orig_ind = cancernew['gdc_cases.samples.portions.analytes.aliquots.submitter_id'].index[dc[2]]
    cancernew['size2'].iloc[orig_ind] = [sizes[i]] * len(orig_ind)
    cancernew['link2'].iloc[orig_ind] = linkstrant.values
    cancernew['ss'].iloc[orig_ind] = 1
    # Add missing samples
    a = np.setdiff1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24], df['gdc_cases.samples.portions.analytes.aliquots.submitter_id'].str[:16])
    print(len(a))
    b = np.intersect1d([aa[:-4] for aa in a], luad_df.bcr_patient_barcode.values, return_indices=True)
    noclinical = np.setdiff1d(range(len(a)), b[1])
    #a = np.setdiff1d(a, a[noclinical])
    #c = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24].values, b[0], return_indices=True)
    if noclinical.size ==0:
        c = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24].values, a, return_indices=True)
    elif noclinical.size >0:
        c = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:20].values, b[0], return_indices=True)
    linkstr = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[c[1]]
    if len(b[0]) == len(a):
        print('All good')
    dataadd = {'gdc_cases.samples.portions.analytes.aliquots.submitter_id': a[b[1]],
    'gdc_cases.demographic.gender': luad_df.gender.iloc[b[2]].values,
    'gdc_cases.demographic.race': luad_df.race.iloc[b[2]].values}
    dataadd['gdc_cases.demographic.ethnicity'] = luad_df.ethnicity.iloc[b[2]].values
    if tumorID == 'LIHC':
        dataadd['gdc_cases.exposures.weight'] = luad_df.weight_kg_at_diagnosis.iloc[b[2]].values
        dataadd['gdc_cases.exposures.height'] = luad_df.height_cm_at_diagnosis.iloc[b[2]].values
        dataadd['gdc_cases.diagnoses.primary_diagnosis'] = luad_df.histologic_diagnosis.iloc[b[2]].values
    elif tumorID == 'BRCA':
        dataadd['gdc_cases.exposures.weight'] = 'NA'
        dataadd['gdc_cases.exposures.height'] = 'NA'
        dataadd['gdc_cases.diagnoses.primary_diagnosis'] = luad_df.histologic_diagnosis_other.iloc[b[2]].values
    dataadd['gdc_cases.project.primary_site'] = luad_df.tumor_tissue_site.iloc[b[2]].values
    dataadd['cgc_case_age_at_diagnosis'] = luad_df.age_at_initial_pathologic_diagnosis.iloc[b[2]].values
    dataadd['gdc_cases.diagnoses.tumor_stage']   = luad_df.ajcc_pathologic_tumor_stage.iloc[b[2]].values
    dataadd['gdc_cases.diagnoses.days_to_death'] = luad_df.death_days_to.iloc[b[2]].values
    dataadd['gdc_cases.diagnoses.vital_status']  = luad_df.vital_status.iloc[b[2]].values
    dataadd['subtype'] = "NA"
    dataadd['link2'] = linkstr
    dataadd['size2'] = [sizes[i]] * len(b[0])
    dataadd['ss'] = [1] * len(b[0])
    concatdf = pd.DataFrame(dataadd)
    if noclinical.size >0: # put back the missing sample
        toadd = ['NA'] * (concatdf.shape[1])
        toadd[0] = a[noclinical][0]
        toadd[-1] = 1
        toadd[-2] = sizes[i]
        cc = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24].values, a[noclinical], return_indices=True)
        stradd = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[cc[1]]
        toadd[-3] = stradd.iloc[0]
        concatdf.loc[-1] = toadd
    cancernew = pd.concat((cancernew, concatdf))
    # add clean name
    cancernew['submitter_id_clean'] = tumorID + '_' + cancernew['link2'].str.split('/').str[-1].str[:-3].str.replace('-', '_')
    # part 2
    cancernew.to_csv('~/granddb/static/data/pancreas_tcga_bis.csv', index=False)
    i = i + 1



# Now COAD
tumorIDs = ['COAD']
sizes = ['82.9 MB']
tissues = ['colon']

i=0
for tumorID in tumorIDs:
    print(tumorID)
    df = pd.read_csv('~/granddb/static/data/clinical_tcga.csv')
    cancernew = df.copy()
    cancernew['ss'] = 0
    cancernew['size2'] = 0
    cancernew['link2'] = '-'
    luad_df = pd.read_csv('~/Downloads/clinical_patient_' + tumorID.lower() + '.csv')
    # Add link and size to existing samples
    dc = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24],
                        cancernew['sample'].str[:16], return_indices=True)
    linkstrant = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + \
                 '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[dc[1]]
    orig_ind = cancernew['sample'].index[dc[2]]
    cancernew['size2'].iloc[orig_ind] = [sizes[i]] * len(orig_ind)
    cancernew['link2'].iloc[orig_ind] = linkstrant.values
    cancernew['ss'].iloc[orig_ind] = 1
    # Add missing samples
    a = np.setdiff1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24], df['sample'].str[:16])
    print(len(a))
    b = np.intersect1d([aa[:-4] for aa in a], luad_df.bcr_patient_barcode.values, return_indices=True)
    noclinical = np.setdiff1d(range(len(a)), b[1])
    if noclinical.size ==0:
        c = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24].values, a, return_indices=True)
    elif noclinical.size >0:
        c = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:20].values, b[0], return_indices=True)
    linkstr = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[c[1]]
    if len(b[0]) == len(a):
        print('All good')
    dataadd = {'sample': a[b[1]],
    'gender': luad_df.gender.iloc[b[2]].values,
    'race': luad_df.race.iloc[b[2]].values}
    dataadd['platform'] = ['NA'] * len(b[0])
    dataadd['weight_kg_at_diagnosis'] = luad_df.weight_kg_at_diagnosis.iloc[b[2]].values
    dataadd['height_cm_at_diagnosis'] = luad_df.height_cm_at_diagnosis.iloc[b[2]].values
    dataadd['anatomic_neoplasm_subdivision'] = luad_df.anatomic_neoplasm_subdivision.iloc[b[2]].values
    dataadd['age_at_initial_pathologic_diagnosis'] = luad_df.age_at_initial_pathologic_diagnosis.iloc[b[2]].values
    dataadd['uicc_stage']   = luad_df.ajcc_pathologic_tumor_stage.iloc[b[2]].values
    dataadd['time_to_event'] = 'NA'
    dataadd['vital_status']  = luad_df.vital_status.iloc[b[2]].values
    dataadd['subtype'] = "NA"
    dataadd['link2'] = linkstr
    dataadd['size2'] = [sizes[i]] * len(b[0])
    dataadd['ss'] = [1] * len(b[0])
    concatdf = pd.DataFrame(dataadd)
    if noclinical.size >0: # put back the missing samples
        for ij in range(noclinical.size):
            toadd = ['NA'] * (concatdf.shape[1])
            toadd[0] = a[noclinical][ij]
            toadd[-1] = 1
            toadd[-2] = sizes[i]
            cc = np.intersect1d(tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].str[8:24].values, a[noclinical[ij]], return_indices=True)
            stradd = 'https://granddb.s3.us-east-2.amazonaws.com/cancer/' + tissues[i] + '_cancer/lioness_tcga_' + tumorID.lower() + '/' + tcganfdf[tcganfdf['tumorID'] == tumorID]['net'].iloc[cc[1]]
            toadd[-3] = stradd.iloc[0]
            concatdf.loc[-(ij+1)] = toadd
    cancernew = pd.concat((cancernew, concatdf))
    # add clean name
    cancernew['submitter_id_clean'] = tumorID + '_' + cancernew['link2'].str.split('/').str[-1].str[:-3].str.replace('-', '_')
    # part 2
    cancernew.to_csv('~/granddb/static/data/clinical_tcga_bis.csv', index=False)
    i = i + 1

