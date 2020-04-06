import pandas as pd
import os
import numpy as np

if __name__ == '__main__':
    #os.chdir('../../granddb/src/diseaseEnr')
    disease = pd.read_csv('TF-disease-data_Fig4_disease.csv')
    disease.columns =['Phenotype Name', ' -log P-value', 'P-value', 'Count', 'TF genes',
           'hpoId', 'Unnamed: 6', 'Unnamed: 7']
    disease_copy = disease.copy()
    hpo     = pd.read_csv('genes_to_phenotype.txt',sep='\t',comment='#')

    k=0
    disease['Phenotype Name'].iloc[664] = 'Long eyelashes'
    disease['Phenotype Name'].iloc[670] = 'Ragged-red muscle fibers'
    disease['Phenotype Name'].iloc[705] = 'Decreased proportion circulating T-helper cells'
    disease['Phenotype Name'].iloc[714] = 'Abnormal corneal endothelium morphology'
    disease['Phenotype Name'].iloc[718] = 'Strabismus'
    disease['Phenotype Name'].iloc[734] = 'Myxoid subcutaneous tumors'
    disease['Phenotype Name'].iloc[760] = 'Abnormal left ventricle morphology'
    disease['Phenotype Name'].iloc[773] = 'Abnormal muscle fiber morphology'
    disease['Phenotype Name'].iloc[779] = 'Prostate cancer'
    disease['Phenotype Name'].iloc[794] = 'Abnormal reticulocyte morphology'
    disease['Phenotype Name'].iloc[795] = 'Abnormal natural killer cell morphology'
    disease['Phenotype Name'].iloc[837] = 'Neutropenia in presence of anti-neutropil antibodies'
    disease['Phenotype Name'].iloc[860] = 'Increased circulating IgA level'
    disease['Phenotype Name'].iloc[892] = 'Abnormality iris morphology'
    disease['Phenotype Name'].iloc[895] = 'Abnormal intestine morphology'
    disease['Phenotype Name'].iloc[938] = 'Increased circulating IgM level'
    disease['Phenotype Name'].iloc[978] = 'Displacement of the urethral meatus'
    disease['Phenotype Name'].iloc[984] = 'Neutropenia'
    disease['Phenotype Name'].iloc[1010] = 'Abnormal renal collecting system morphology'
    disease['Phenotype Name'].iloc[1011] = 'Recurrent herpes'
    disease['Phenotype Name'].iloc[1021] = 'Reduced circulating prolactin concentration'
    disease['Phenotype Name'].iloc[1095] = 'Abnormal conjunctiva morphology'
    disease['Phenotype Name'].iloc[1136] = 'Abnormal cardiac septum morphology'
    disease['Phenotype Name'].iloc[1142] = 'Abnormal morphology of female internal genitalia'
    disease['Phenotype Name'].iloc[1167] = 'Abnormal anterior chamber morphology'
    disease['Phenotype Name'].iloc[1182] = 'High hypermetropia'
    disease['Phenotype Name'].iloc[1221] = 'Abnormal nasolacrimal system morphology'
    disease['Phenotype Name'].iloc[1230] = 'Abnormal cerebral morphology'
    disease['Phenotype Name'].iloc[1235] = 'Skin dimple'
    disease['Phenotype Name'].iloc[1251] = 'Hemeralopia'
    disease['Phenotype Name'].iloc[1257] = 'Recurrent viral infections'
    disease['Phenotype Name'].iloc[1259] = 'Abnormal soft palate morphology'
    disease['Phenotype Name'].iloc[1275] = 'Abnormal basophil morphology'
    disease['Phenotype Name'].iloc[1281] = 'High serum calcitriol'
    disease['Phenotype Name'].iloc[1313] = 'Glucose intolerance'
    disease['Phenotype Name'].iloc[1322] = 'Abnormal megakaryocyte morphology'
    disease['Phenotype Name'].iloc[1350] = 'Abnormal vagina morphology'
    disease['Phenotype Name'].iloc[1353] = 'Epiphora'
    disease['Phenotype Name'].iloc[1363] = 'Abnormal fingernail morphology'
    disease['Phenotype Name'].iloc[1376] = 'Abnormal endocardium morphology'
    disease['Phenotype Name'].iloc[1389] = 'Abnormal oral cavity morphology'
    disease['Phenotype Name'].iloc[1413] = 'Low levels of vitamin B1'
    disease['Phenotype Name'].iloc[1454] = 'Abnormal tracheobronchial morphology'
    disease['Phenotype Name'].iloc[1473] = 'Low levels of vitamin A'
    disease['Phenotype Name'].iloc[1474] = 'Low levels of vitamin E'
    disease['Phenotype Name'].iloc[1499] = 'Abnormal aortic arch morphology'
    disease['Phenotype Name'].iloc[1510] = 'Mucoid extracellular matrix accumulation'
    disease['Phenotype Name'].iloc[1516] = 'Generalized myoclonic seizure'
    disease['Phenotype Name'].iloc[1519] = 'Abnormal palate morphology'
    disease['Phenotype Name'].iloc[1530] = 'Abnormal hair morphology'
    disease['Phenotype Name'].iloc[1590] = 'Abnormal distal phalanx morphology of finger'
    disease['Phenotype Name'].iloc[1599] = 'Abnormal thumb morphology'
    disease['Phenotype Name'].iloc[1614] = 'Abnormal adipose tissue morphology'
    disease['Phenotype Name'].iloc[1621] = 'Congenital aphakia'
    disease['Phenotype Name'].iloc[1645] = 'Abdominal aortic aneurysm'
    disease['Phenotype Name'].iloc[1647] = 'Ascending tubular aorta aneurysm'
    disease['Phenotype Name'].iloc[1690] = 'High myopia'
    disease['Phenotype Name'].iloc[1700] = 'Low levels of vitamin K'
    disease['Phenotype Name'].iloc[1703] = 'Abnormal cornea morphology'
    disease['Phenotype Name'].iloc[1708] = 'Limbal dermoid'
    disease['Phenotype Name'].iloc[1725] = 'Abnormal calcium-phosphate regulating hormone level'
    disease['Phenotype Name'].iloc[1762] = 'Abnormal pupil morphology'
    disease['Phenotype Name'].iloc[1801] = 'Abnormally ossified vertebrae'
    disease['Phenotype Name'].iloc[1818] = 'Low levels of vitamin D'
    disease['Phenotype Name'].iloc[1840] = 'Abnormal proportion of CD4 T cells'
    disease['Phenotype Name'].iloc[1867] = 'Simplified gyral pattern'
    disease['Phenotype Name'].iloc[1873] = 'Abnormal retinal vascular morphology'
    disease['Phenotype Name'].iloc[1895] = 'Abnormal oral frenulum morphology'
    disease['Phenotype Name'].iloc[1930] = 'Left ventricular dysfunction'
    disease['Phenotype Name'].iloc[1954] = 'Abnormal fallopian tube morphology'
    disease['Phenotype Name'].iloc[1957] = 'Eyelid coloboma'
    disease['Phenotype Name'].iloc[1963] = 'Abnormal heart valve morphology'
    disease['Phenotype Name'].iloc[1968] = 'Irregular menstruation'
    disease['Phenotype Name'].iloc[1973] = 'Coronary artery atherosclerosis'
    disease['Phenotype Name'].iloc[2017] = 'Abnormal tubulointerstitial morphology'
    disease['Phenotype Name'].iloc[2024] = 'Color vision defect'
    disease['Phenotype Name'].iloc[2049] = 'Abnormal thrombocyte morphology'
    disease['Phenotype Name'].iloc[2060] = 'Ascending tubular aorta aneurysm'
    disease['Phenotype Name'].iloc[2067] = 'Abnormal cerebellum morphology'
    disease['Phenotype Name'].iloc[2074] = 'Vitreoretinopathy'
    disease['Phenotype Name'].iloc[2080] = 'Seizure'
    disease['Phenotype Name'].iloc[2119] = 'Pigmentary retinopathy'
    disease['Phenotype Name'].iloc[2123] = 'Increased circulating total IgE level'
    disease['Phenotype Name'].iloc[2125] = 'Ocular hypertension'
    disease['Phenotype Name'].iloc[2142] = 'Elevated hepatic transaminase'
    disease['Phenotype Name'].iloc[2144] = 'Severely reduced visual acuity'
    disease['Phenotype Name'].iloc[2146] = 'Decreased circulating IgG level'
    disease['Phenotype Name'].iloc[2152] = 'Abnormally large globe'
    disease['Phenotype Name'].iloc[2156] = 'Abnormal lymphocyte morphology'
    disease['Phenotype Name'].iloc[2160] = 'Decreased HDL cholesterol concentration'
    disease['Phenotype Name'].iloc[2199] = 'Abnormal aortic valve morphology'
    disease['Phenotype Name'].iloc[2239] = 'Aortic aneurysm'
    disease['Phenotype Name'].iloc[2241] = 'Abnormal testis morphology'
    disease['Phenotype Name'].iloc[2248] = 'Renal tubular atrophy'
    disease['Phenotype Name'].iloc[2277] = 'Onychogryposis'
    disease['Phenotype Name'].iloc[2287] = 'Sparse hair'
    disease['Phenotype Name'].iloc[2308] = 'Aplastic clavicle'
    disease['Phenotype Name'].iloc[66] = 'Hypogonadotropic hypogonadism'
    disease['Phenotype Name'].iloc[90] = 'Ocular anterior segment dysgenesis'
    disease['Phenotype Name'].iloc[186] = 'Aortic arch aneurysm'
    disease['Phenotype Name'].iloc[194] = 'Decreased serum testosterone level'
    disease['Phenotype Name'].iloc[201] = 'Abnormal sacrum morphology'
    disease['Phenotype Name'].iloc[212] = 'Primary congenital glaucoma'
    disease['Phenotype Name'].iloc[218] = 'Abnormality of glycosphingolipid metabolism'
    disease['Phenotype Name'].iloc[231] = 'Impaired sensitivity to thyroid hormone'
    disease['Phenotype Name'].iloc[239] = 'Abnormal autonomic nervous system physiology'
    disease['Phenotype Name'].iloc[252] = 'Abnormal cranial nerve morphology'
    disease['Phenotype Name'].iloc[313] = 'Abnormal granulocytopoietic cell morphology'
    disease['Phenotype Name'].iloc[319] = 'Abnormal Descemet membrane morphology'
    disease['Phenotype Name'].iloc[410] = 'Abnormal lacrimal duct morphology'
    disease['Phenotype Name'].iloc[426] = 'Abnormal left ventricular outflow tract morphology'
    disease['Phenotype Name'].iloc[486] = 'Premature coronary artery atherosclerosis'
    disease['Phenotype Name'].iloc[505] = 'Abnormal circulating fatty-acid concentration'
    disease['Phenotype Name'].iloc[545] = 'Abnormal autonomic nervous system physiology'
    disease['Phenotype Name'].iloc[601] = 'Erectile dysfunction'
    disease['Phenotype Name'].iloc[657] = 'Increased circulating free T3'




    t=0
    for diseaseTerm in disease['Phenotype Name']:
        indDisease=np.where(diseaseTerm == hpo.iloc[:,3])
        if len(indDisease[0])==0:
            newterm=diseaseTerm + ' morphology'
            indDisease = np.where(newterm == hpo.iloc[:, 3])
            if len(indDisease[0]) == 0:
                print(diseaseTerm)
                print(k)
                t=t+1
            else:
                print('fixed!')
        selectedTerm=hpo.iloc[indDisease[0][0],2]
        disease.iloc[k,5] = selectedTerm[0:2].upper() + selectedTerm[2:]
        k=k+1

    disease_copy['hpoId'] = disease['hpoId']
    disease_copy.to_csv('TF-disease-data_Fig4_disease.csv',index=0)



a=time.time()
aa=pd.read_csv('Intestine_Terminal_Ileum_AllSamples.csv',usecols=[0],sep=',',header=0,nrows=19476492)
b=time.time()-a




import pandas as pd
import dask.dataframe as dd
import time
import numpy as np



df_train = dd.read_csv('Intestine_Terminal_Ileum_AllSamples.csv', usecols=[1])
df_train=df_train.compute()
tfs=pd.read_csv('tissue_tfs.csv',header=None)
genes=pd.read_csv('tissue_genes.csv',header=None)
tfs.columns = ['','']
genes.columns = ['','']
xx=pd.DataFrame(index=tfs.iloc[1:,1],columns=genes.iloc[:,1],data=df_train.iloc[:,0].values.reshape((644,30243)))
#file name is sample name

TotalGb=256+219+154+142+126+119+119+118+117+110+110+94+88+84+82+78+72+72+68+67+64+59+58+53+47+45+41+39+34


import boto3
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('granddb')
for my_bucket_object in my_bucket.objects.filter(Prefix='tissues/networks/lioness/singleSample/'):
    if my_bucket_object.key=='tissues/networks/lioness/singleSample/Adipose_subcutaneous_tissue_sample40_GTEX-13QBU-1926-SM-5IJEW.csv':
        print('file exist')


#Adipose_subcutaneous_tissue_sample40_GTEX-13QBU-1926-SM-5IJEW.csv