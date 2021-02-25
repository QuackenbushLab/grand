import os

os.system('rm db.sqlite3')
os.system('python3 manage.py makemigrations')
os.system('python3 manage.py migrate')
data=['load_cell_data','load_tissue_data','load_drugResultDown_data','load_drugResultUp_data','load_gwas_data','load_disease_data','load_params_data','load_tissue-target_data',
	'load_tissue-expression_data','load_tissuelanding_data','load_druglanding_data','load_tissueSampleInfo_data','load_cancerlanding_data',
        'load_cancertcga_data','load_cancergeo_data','load_gene_data','load_drugSample','load_drugDesc','load_cancer_data','load_cancerbreast_data',
        'load_cancercervix_data','load_cancerliver_data','load_gbmd1_data','load_gbmd2_data','load_cancerggn_data']

for i in range(len(data)):
   os.system('python3 manage.py ' + data[i])
