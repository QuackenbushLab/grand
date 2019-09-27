import os

os.system('rm db.sqlite3')
os.system('python3 manage.py makemigrations')
os.system('python3 manage.py migrate')
data=['load_drug_data','load_cell_data','load_tissue_data','load_drugResultDown_data','load_drugResultUp_data','load_gwas_data','load_disease_data','load_params_data']

for i in range(len(data)):
   os.system('python3 manage.py ' + data[i])
