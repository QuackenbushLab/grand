import pandas as pd
import numpy as np
import os

os.chdir('/Users/mab8354/netzoopap')

# First read dragon network
# Parameters
imputationMissing='zero'
# 0. Load metadata
cellNames=pd.read_csv('data/sample_info.csv')
# II. MiRna-mRNA
# 1. Read miRNA and mRNA
mirna=pd.read_csv('data/CCLE_miRNA_20181103.gct',sep='\t',comment='#',skiprows=2,index_col=1)
expression=pd.read_csv('data/CCLE_expression.csv',index_col=0)
# 2. remove unnecessary columns
mirna = mirna.iloc[:,1:]
# 3. convert cell names to depmap IDs
mirna=convertToDepMap(mirna,cellNames)
# 4. align dataframes
expression,mirna=alignDF(expression,mirna,remove_std=1)

# Next cell line
os.chdir('/Users/mab8354/')
cellinfo = pd.read_csv('granddb/data/sample_info.csv',index_col=0)
exprs    = pd.read_csv('netzoopap/data/CCLE_expression.csv',index_col=0)
ccleanno = pd.read_csv('granddb/data/Cell_lines_annotations_20181226.txt',sep='\t',index_col=1)
intercells= np.intersect1d(exprs.index, cellinfo.index)
# replace NA
ccleanno.index = ccleanno.index.fillna('')

# Add mutation rate and doubling time
a = np.intersect1d( cellinfo.index, ccleanno.index )
# present in expression
cellinfo['presexp'] = 0
cellinfo['presexp'].loc[intercells] = 1
# mutrate
cellinfo['mutRate'] = np.nan
cellinfo['mutRate'].loc[a] = ccleanno['mutRate'].loc[a]
# doubling time
cellinfo['doublt'] = np.nan
cellinfo['doublt'].loc[a] = ccleanno['Doubling.Time.Calculated.hrs'].loc[a]
#tcga code
cellinfo['tcga'] = '-'
cellinfo['tcga'].loc[a] = ccleanno['tcga_code'].loc[a]
#race
cellinfo['race'] = '-'
cellinfo['race'].loc[a] = ccleanno['Race'].loc[a]
cellinfo['race'].replace()
# size
cellinfo['size'] = '359 MB'
# replace empty
cellinfo['dummy'] = '-'
cellinfo['dummy'].loc[intercells] = 'dragon'
cellinfo.replace(np.nan,
           "-",
           inplace=True)
# differmtillay expressed tfs (bardata from buildDiffReg.py)
cellinfo['diffexp'] = 0
cellinfo['diffexp'].loc[intercells] = bardata.loc[intercells]
cellinfo['difftar'] = 0
cellinfo['difftar'].loc[intercells] = bardatatar.loc[intercells]
cellinfo['difftargenes'] = 0
cellinfo['difftargenes'].loc[intercells] = bardatagenestar.loc[intercells]
cellinfo['diffexpgenes'] = 0
cellinfo['diffexpgenes'].loc[intercells] = bardatagenes.loc[intercells]
# clean names
newname=[]
for name in cellinfo.index:
    newname.append('_'.join(str.split(name,'-')))

cellinfo['cleanname'] = newname

# clean disease names
cellinfo=pd.read_csv('granddb/data/sample_info_aug.csv',index_col=0)
cellinfo['cleannamedis'] =''
validURLs=[]
uniquedisease = cellinfo['primary_disease']
for di in uniquedisease:
    if len(str.split(di, ' '))>1:
        validURLs.append('_'.join(str.split(di, ' ')))
    elif len(str.split(di, '/'))>1:
        validURLs.append('_'.join(str.split(di, '/')))
    elif len(str.split(di, '-'))>1:
        validURLs.append('_'.join(str.split(di, '-')))
    else:
        validURLs.append(di)
# second pass
newValid = []
for di in validURLs:
    if len(str.split(di, ' '))>1:
        newValid.append('_'.join(str.split(di, ' ')))
    elif len(str.split(di, '/'))>1:
        newValid.append('_'.join(str.split(di, '/')))
    elif len(str.split(di, '-'))>1:
        newValid.append('_'.join(str.split(di, '-')))
    else:
        newValid.append(di)
cellinfo['cleannamedis'] = newValid

# filter dragon samples
cellinfo['isdragon'] = '-'
intercellsdragon = np.intersect1d(cellinfo.index, expression.index)
cellinfo['isdragon'].loc[intercellsdragon] = 'dragon'

# save df
cellinfo.to_csv('granddb/data/sample_info_aug2.csv')

# intersect with expression data
intercells= np.intersect1d(exprs.index, cellinfo.index)

cellinfo = cellinfo.loc[intercells]

uniquedisease = np.unique(cellinfo.primary_disease)

ncells = []
for disease in uniquedisease:
    ncells.append(np.sum(cellinfo.primary_disease == disease))

resDf = pd.DataFrame(data=ncells,index=uniquedisease,columns=['ncells'])
resDf.to_csv('granddb/data/cellsinfofilter.csv')

# build df of cells
resDf2 = pd.DataFrame(columns=['tissue'])

resDf2['tissue'] = ['All']
resDf2['method'] = ['DRAGON']
resDf2['data']   = ['CCLE']
resDf2['type']   = ['aggregate']
resDf2['condition']  = ['Cancer']
resDf2['urllinks']   = ['mirna']
resDf2['reg']        = ['miRNA']
resDf2['method2']    = ''

resDf2.loc[len(resDf2.index)] = ['Fibroblast', 'PANDA', 'GTEx', 'aggregate','Normal (primary)','fibroblast_gtex','TF','PUMA']
resDf2.loc[len(resDf2.index)] = ['LCL', 'PANDA', 'GTEx', 'aggregate','Normal (transformed)','lcl','TF','PUMA']

validURLs=[]
for di in uniquedisease:
    if len(str.split(di, ' '))>1:
        validURLs.append('_'.join(str.split(di, ' ')))
    elif len(str.split(di, '/'))>1:
        validURLs.append('_'.join(str.split(di, '/')))
    elif len(str.split(di, '-'))>1:
        validURLs.append('_'.join(str.split(di, '-')))
    else:
        validURLs.append(di)
# second pass
newValid = []
for di in validURLs:
    if len(str.split(di, ' '))>1:
        newValid.append('_'.join(str.split(di, ' ')))
    elif len(str.split(di, '/'))>1:
        newValid.append('_'.join(str.split(di, '/')))
    elif len(str.split(di, '-'))>1:
        newValid.append('_'.join(str.split(di, '-')))
    else:
        newValid.append(di)

resDf3 = pd.DataFrame(columns=['tissue'])
resDf3['tissue']    = uniquedisease
resDf3['method']    = 'LIONESS'
resDf3['data']      = 'CCLE'
resDf3['type']      = 'single-sample'
resDf3['condition'] = 'Cancer'
resDf3['urllinks']  = newValid
resDf3['reg']   = 'TF'

resDf2=resDf2.append(resDf3)
# save df
a=['https://netzoo.github.io/zooanimals/lioness/']*len(uniquedisease)
c=['https://netzoo.github.io/zooanimals/dragon/','https://netzoo.github.io/zooanimals/panda/','https://netzoo.github.io/zooanimals/panda/']
c.extend(a)
b=['https://portals.broadinstitute.org/ccle']*len(uniquedisease)
d=['https://portals.broadinstitute.org/ccle','https://www.gtexportal.org/home/','https://www.gtexportal.org/home/']
d.extend(b)
resDf2['methodrefs'] = c
resDf2['datarefs']   = d
# add refs to PUMA
resDf2['methodrefs2'] = ''
resDf2['methodrefs2'].iloc[1:3] = ['https://netzoo.github.io/zooanimals/puma/','https://netzoo.github.io/zooanimals/puma/']
# add mirna in normal cells
resDf2['reg2'] = ''
resDf2['reg2'].iloc[1:3] = ['miRNA','miRNA']
resDf2.to_csv('granddb/data/cellspage.csv',index=False)


# build cell landing df
colNames=['cancer','cancerref','cancerLink','tool','netzoo','netzooLink','netzooRel','network','ppi','ppiLink','motif','expression',
          'expLink','tfs','genes','refs','samples','cardref','script','dataset','reg']
resDflanding = pd.DataFrame(columns=colNames)
resDflanding['cancer']=uniquedisease
resDflanding['cancerref']= newValid
resDflanding['cancerLink'] = ''
resDflanding['tool'] = 'LIONESS'
resDflanding['netzoo'] = 'netZooPy'
resDflanding['netzooLink'] = 'https://github.com/netZoo/netZooPy/releases'
resDflanding['netzooRel'] = '0.8'
resDflanding['network'] = '#cardtissuetcga'
resDflanding['ppi'] = 'https://granddb.s3.amazonaws.com/optPANDA/ppi/ppi_complete.txt'
resDflanding['ppiLink'] = 'https://string-db.org/'
resDflanding['motif'] = 'https://granddb.s3.us-east-2.amazonaws.com/cells/motif/regMatCont2ProcessedEdges.csv'
resDflanding['expression'] = 'https://granddb.s3.us-east-2.amazonaws.com/cells/expression/CCLE_expression_withinSample.csv'
resDflanding['expLink'] = 'https://portals.broadinstitute.org/ccle'
resDflanding['tfs'] = 1132
resDflanding['genes'] = 18560
resDflanding['refs2'] = 'Ben Guebila et al. (in preparation)'
resDflanding['samples'] = ncells
resDflanding['cardref'] = resDflanding['network']
resDflanding['script'] = 'https://granddb.s3.us-east-2.amazonaws.com/cells/scripts/reproduceccleNetwork.m'
resDflanding['dataset'] = 'CCLE'
resDflanding['reg'] = 'TF'

#add lcl and fibro  and dragon
resDflanding.loc[len(resDflanding.index)] = ['LCL','lcl','','PANDA','netZooM','https://github.com/netZoo/netZooM/releases','0.1'
    ,'','','','','','',0,0,'Lopes-Ramos, Paulsson et al. (2017)',0,'','','GTEX','','TF']
resDflanding.loc[len(resDflanding.index)] = ['Fibroblast','fibroblast','','PANDA','netZooM','https://github.com/netZoo/netZooM/releases','0.1'
    ,'','','','','','',0,0,'Lopes-Ramos, Paulsson et al. (2017)',0,'','','GTEX','','TF']
resDflanding.loc[len(resDflanding.index)] = ['All','mirna','','DRAGON','netZooPy','https://github.com/netZoo/netZooPy/releases','0.8'
    ,'https://granddb.s3.us-east-2.amazonaws.com/cells/networks/mirna/dragon_mirna_CCLE.csv','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/CCLE_miRNA_20181103.gct','https://portals.broadinstitute.org/ccle','','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/CCLE_expression.csv','https://portals.broadinstitute.org/ccle',734,19174,'',938,'#cardtissuetcga','https://github.com/netZoo/netbooks/blob/main/netbooks/netZooPy/dragon_mirna.ipynb','CCLE','miRNA','Ben Guebila et al. (in preparation)']
# add vis link
resDflanding['cancerLink'] = '/networks/aggregate/colon_cancer1/'
resDflanding.to_csv('granddb/data/celllanding.csv',index=False)

d = {'TF': ['TF'], 'tar': [1]}
tftarscore = pd.DataFrame(data=d)



a=pd.read_csv('/Users/mab8354/Downloads/PANDA_ACC.csv',index_col=0)
b=pd.read_csv('/Users/mab8354/Downloads/Adipose_Subcutaneous.csv',index_col=0)
c=a-b
intergenes = np.intersect1d(a.columns,b.columns)
c=c[intergenes]
