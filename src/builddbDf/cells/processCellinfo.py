import pandas as pd
import numpy as np
import os, sys
from compareCorrs import convertToDepMap,alignDF

# set path
os.chdir('/Users/mab8354/netzoopap')

#functions
def computenewValid(uniquedisease):
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
    return newValid

# First read dragon network
# Parameters
imputationMissing='zero'
# 0. Load metadata
cellNames=pd.read_csv('data/sample_info.csv')
# II. MiRna-mRNA
# 1. Read miRNA and mRNA
mirna     =pd.read_csv('data/CCLE_miRNA_20181103.gct',sep='\t',comment='#',skiprows=2,index_col=1)
expression=pd.read_csv('data/CCLE_expression.csv',index_col=0)
# 2. remove unnecessary columns
mirna = mirna.iloc[:,1:]
# 3. convert cell names to depmap IDs (function from compareCorrs.py)
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
# differentillay expressed tfs (bardata from buildDiffReg.py)
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

uniquedisease = cellinfo['primary_disease']
newValid= computenewValid(uniquedisease)

cellinfo['cleannamedis'] = newValid

# filter dragon samples
cellinfo['isdragon'] = '-'
intercellsdragon = np.intersect1d(cellinfo.index, expression.index)
cellinfo['isdragon'].loc[intercellsdragon] = 'dragon'

# save df
cellinfo.to_csv('granddb/data/sample_info_aug2.csv')
#cellinfo=pd.read_csv('~/granddb/data/sample_info_aug2.csv', index_col=0)

##################################
#### build cell line data ########
##################################
# intersect with expression data
intercells= np.intersect1d(exprs.index, cellinfo.index)

cellinfo = cellinfo.loc[intercells]

uniquedisease = np.unique(cellinfo.primary_disease)

def buildcellnofilter(uniquedisease):
    ncells = []
    for disease in uniquedisease:
        ncells.append(np.sum(cellinfo.primary_disease == disease))

    resDf = pd.DataFrame(data=ncells,index=uniquedisease,columns=['ncells'])
    resDf.index.name = 'disease'
    resDf.to_csv('granddb/data/cellsinfofilter.csv')
    return ncells
ncells=buildcellnofilter(uniquedisease)

# compute new valid
newValid = computenewValid(uniquedisease)
def buildcellspage(uniquedisease,newValid):
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

    # Add EGRET
    resDf2.loc[len(resDf2.index)] = ['IPSC','EGRET','Banovich et al.','aggregate','Normal','ipsc','TF','PANDA','https://netzoo.github.io/zooanimals/egret/','https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE89895','https://netzoo.github.io/zooanimals/panda/','']
    resDf2.loc[len(resDf2.index)] = ['IPSC-Cardiomyocyte','EGRET','Banovich et al.','aggregate','Normal','cm','TF','PANDA','https://netzoo.github.io/zooanimals/egret/','https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE89895','https://netzoo.github.io/zooanimals/panda/','']
    #reindex
    resDf2.index = range(0,resDf2.shape[0])
    #modify LCL banovich
    resDf2.loc[np.where(resDf2['tissue']=='LCL')[0][0],'method3'] = 'EGRET'
    resDf2.loc[np.where(resDf2['tissue']=='LCL')[0][0],'methodrefs3'] = 'https://netzoo.github.io/zooanimals/egret/'
    # Add EGRET K562
    resDf2.loc[len(resDf2.index)] = ['K562','EGRET','ENCODE','aggregate','Normal','k562','TF','EGRET','https://netzoo.github.io/zooanimals/egret/','https://www.encodeproject.org/','','','','']
    resDf2.loc[len(resDf2.index)] = ['GM12878','EGRET','ENCODE','aggregate','Normal','gm12878','TF','EGRET','https://netzoo.github.io/zooanimals/egret/','https://www.encodeproject.org/','','','','']

    resDf2.to_csv('granddb/data/cellspage.csv',index=False)
    return
# build cellspage
buildcellspage(uniquedisease,newValid)

# build cell landing df
def saveCellLanding(uniquedisease, newValid):
    colNames=['cancer','cancerref','cancerLink','tool','netzoo','netzooLink','netzooRel','network','ppi','ppiLink','motif','expression',
              'expLink','tfs','genes','refs','samples','cardref','script','dataset','reg']
    resDflanding = pd.DataFrame(columns=colNames)
    resDflanding['cancer']     = uniquedisease
    resDflanding['cancerref']  = newValid
    resDflanding['cancerLink'] = ''
    resDflanding['tool']   = 'LIONESS'
    resDflanding['netzoo'] = 'netZooM'
    resDflanding['netzooLink'] = 'https://github.com/netZoo/netZooM/releases'
    resDflanding['netzooRel']  = '0.5.3'
    resDflanding['network']    = '#cardtissue'
    resDflanding['ppi']     = 'https://granddb.s3.amazonaws.com/optPANDA/ppi/ppi_complete.txt'
    resDflanding['ppiLink'] = 'https://string-db.org/'
    resDflanding['motif']   = 'https://granddb.s3.us-east-2.amazonaws.com/cells/motif/regMatCont2ProcessedEdges.csv'
    resDflanding['expression'] = 'https://granddb.s3.us-east-2.amazonaws.com/cells/expression/CCLE_expression_withinSample.csv'
    resDflanding['expLink']    = 'https://portals.broadinstitute.org/ccle'
    resDflanding['tfs'] = 1132
    resDflanding['genes'] = 18560
    resDflanding['refs2'] = 'Please check the reference Ben Guebila et al. (2023) at the following link.'
    resDflanding['samples'] = ncells
    resDflanding['cardref'] = resDflanding['network']
    resDflanding['script']  = 'https://granddb.s3.us-east-2.amazonaws.com/cells/scripts/reproduceccleNetwork.m'
    resDflanding['dataset'] = 'CCLE'
    resDflanding['reg']     = 'TF'
    resDflanding['genotype']= '-'
    resDflanding['qbic']    = '-'
    resDflanding['eqtl']    = '-'
    #add lcl and fibro  and dragon
    #resDflanding.loc[len(resDflanding.index)] = ['LCL','lcl','','PANDA','netZooM','https://github.com/netZoo/netZooM/releases','0.1'
    #    ,'','','','','','',0,0,'Lopes-Ramos, Paulsson et al. (2017)',0,'','','GTEX','','TF','','','']
    #resDflanding.loc[len(resDflanding.index)] = ['Fibroblast','fibroblast','','PANDA','netZooM','https://github.com/netZoo/netZooM/releases','0.1'
    #    ,'','','','','','',0,0,'Lopes-Ramos, Paulsson et al. (2017)',0,'','','GTEX','','TF','','','']
    resDflanding.loc[len(resDflanding.index)] = ['All','mirna','','DRAGON','netZooPy','https://github.com/netZoo/netZooPy/releases','0.8'
        ,'https://granddb.s3.us-east-2.amazonaws.com/cells/networks/mirna/dragon_mirna_CCLE.csv','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/CCLE_miRNA_20181103.gct','https://portals.broadinstitute.org/ccle','','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/CCLE_expression.csv','https://portals.broadinstitute.org/ccle',734,19174,'',938,'#cardtissuetcga','https://github.com/netZoo/netbooks/blob/main/netbooks/netZooPy/dragon_mirna.ipynb','CCLE','miRNA','Ben Guebila et al. (in preparation)','','','']
    # Add EGRET IPSC
    resDflanding.loc[len(resDflanding.index)] = ['IPSC','ipsc','','EGRET','netZooR','https://github.com/netZoo/netZooR/releases','0.9'
        ,'#cardtissue','https://granddb.s3.us-east-2.amazonaws.com/cells/ppi/EGRET_ppi.txt','http://string90.embl.de/','https://granddb.s3.us-east-2.amazonaws.com/cells/motif/EGRET_motif_prior.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/banovich_iPSC_expression.csv','https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE89895',687,9394,'',119,'#cardtissue','https://github.com/netZoo/netbooks/blob/main/netbooks/netZooR/egret_banovich_netbook.ipynb','Banovich et al.','TF','Weighill et al. (2022)','https://granddb.s3.us-east-2.amazonaws.com/cells/genotype/genotypesYRI.gen.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/qbic/qbic_banovich_iPSC_allModels_smart1.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/eqtl/iPSC_eQTL_in_motif_promotor_adjacent_egene_banovich_finalEGRET_v1_06172020.txt']
    resDflanding.loc[len(resDflanding.index)] = ['IPSC','ipsc','','PANDA','netZooR','https://github.com/netZoo/netZooR/releases','0.9'
        ,'https://granddb.s3.us-east-2.amazonaws.com/cells/networks/iPSC/PANDA_iPSC_Yoruba.csv','https://granddb.s3.us-east-2.amazonaws.com/cells/ppi/EGRET_ppi.txt','http://string90.embl.de/','https://granddb.s3.us-east-2.amazonaws.com/cells/motif/EGRET_motif_prior.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/banovich_iPSC_expression.csv','https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE89895',687,9394,'',119,'/networks/aggregate/PANDA_iPSC_Yoruba/','https://github.com/netZoo/netbooks/blob/main/netbooks/netZooR/egret_banovich_netbook.ipynb','Banovich et al.','TF','Weighill et al. (2022)','-','-','-']
    # Add EGRET IPSC-cm
    resDflanding.loc[len(resDflanding.index)] = ['IPSC-CM','cm','','EGRET','netZooR','https://github.com/netZoo/netZooR/releases','0.9'
        ,'#cardtissue','https://granddb.s3.us-east-2.amazonaws.com/cells/ppi/EGRET_ppi.txt','http://string90.embl.de/','https://granddb.s3.us-east-2.amazonaws.com/cells/motif/EGRET_motif_prior.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/banovich_LCL_expression.csv','https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE89895',687,18855,'https://genome.cshlp.org/content/32/3/524.short',119,'#cardtissue','https://github.com/netZoo/netbooks/blob/main/netbooks/netZooR/egret_banovich_netbook.ipynb','Banovich et al.','TF','Weighill et al. (2022)','https://granddb.s3.us-east-2.amazonaws.com/cells/genotype/genotypesYRI.gen.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/qbic/qbic_banovich_iPSC-CM_allModels_smart1.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/eqtl/iPSCCM_eQTL_in_motif_promotor_adjacent_egene_banovich_finalEGRET_v1_06172020.txt']
    resDflanding.loc[len(resDflanding.index)] = ['IPSC-CM','cm','','PANDA','netZooR','https://github.com/netZoo/netZooR/releases','0.9'
        ,'https://granddb.s3.us-east-2.amazonaws.com/cells/networks/CM/PANDA_CM_Yoruba.csv','https://granddb.s3.us-east-2.amazonaws.com/cells/ppi/EGRET_ppi.txt','http://string90.embl.de/','https://granddb.s3.us-east-2.amazonaws.com/cells/motif/EGRET_motif_prior.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/banovich_iPSC-CM_expression.csv','https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE89895',687,18855,'',119,'/networks/aggregate/PANDA_CM_Yoruba/','https://github.com/netZoo/netbooks/blob/main/netbooks/netZooR/egret_banovich_netbook.ipynb','Banovich et al.','TF','Weighill et al. (2022)','-','-','-']
    # Add EGRET LCL
    resDflanding.loc[len(resDflanding.index)] = ['LCL','lcl','','EGRET','netZooR','https://github.com/netZoo/netZooR/releases','0.9'
        ,'#cardtissueegret','https://granddb.s3.us-east-2.amazonaws.com/cells/ppi/EGRET_ppi.txt','http://string90.embl.de/','https://granddb.s3.us-east-2.amazonaws.com/cells/motif/EGRET_motif_prior.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/banovich_LCL_expression.csv','https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE89895',687,10198,'https://genome.cshlp.org/content/32/3/524.short',119,'#cardtissueegret','https://github.com/netZoo/netbooks/blob/main/netbooks/netZooR/egret_banovich_netbook.ipynb','Banovich et al.','TF','Weighill et al. (2022)','https://granddb.s3.us-east-2.amazonaws.com/cells/genotype/genotypesYRI.gen.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/qbic/qbic_eQTLS_GM12878_K562_finalEGRET_v1_06302020_allModels_smart1.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/eqtl/LCL_eQTL_in_motif_promotor_adjacent_egene_banovich_finalEGRET_v1_06172020.txt']
    resDflanding.loc[len(resDflanding.index)] = ['LCL','lcl','','PANDA','netZooR','https://github.com/netZoo/netZooR/releases','0.9'
        ,'hhttps://granddb.s3.us-east-2.amazonaws.com/cells/networks/LCL/PANDA_LCL_Yoruba.csv','https://granddb.s3.us-east-2.amazonaws.com/cells/ppi/EGRET_ppi.txt','http://string90.embl.de/','https://granddb.s3.us-east-2.amazonaws.com/cells/motif/EGRET_motif_prior.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/banovich_LCL_expression.csv','https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE89895',687,10198,'',119,'/networks/aggregate/PANDA_LCL_Yoruba/','https://github.com/netZoo/netbooks/blob/main/netbooks/netZooR/egret_banovich_netbook.ipynb','Banovich et al.','TF','Weighill et al. (2022)','-','-','-']
    # add tissue
    resDflanding['tissue']   = 'Lymphoblastoid cell line'
    # add data link
    resDflanding['datalink'] = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE89895'
    # add cell link
    resDflanding['vis'] = resDflanding['cardref']
    # Add EGRET k562 and GM12878
    resDflanding.loc[len(resDflanding.index)] = ['K562','k562','https://www.encodeproject.org/files/ENCFF538YDL/','EGRET','netZooR','https://github.com/netZoo/netZooR/releases','0.9'
        ,'https://granddb.s3.us-east-2.amazonaws.com/data/EGRET_K562.csv','https://granddb.s3.us-east-2.amazonaws.com/cells/ppi/EGRET_ppi.txt','http://string90.embl.de/','https://granddb.s3.us-east-2.amazonaws.com/cells/motif/EGRET_motif_prior.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/LCL_expression.csv','https://www.gtexportal.org/home/datasets',687,22936,'https://genome.cshlp.org/content/32/3/524.short',130,'#cardtissue','https://github.com/netZoo/netbooks/blob/main/netbooks/netZooR/egret_banovich_netbook.ipynb','GTEx','TF','Weighill et al. (2022)','https://granddb.s3.us-east-2.amazonaws.com/cells/genotype/K562_formatted.vcf','https://granddb.s3.us-east-2.amazonaws.com/cells/qbic/qbic_eQTLS_GM12878_K562_finalEGRET_v1_06302020_allModels_smart1.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/eqtl/eQTL_in_motif_promotor_adjacent_egene_finalEGRET_v1_06172020.txt','K562','https://www.gtexportal.org/home/datasets','/networks/aggregate/EGRET_K562_Cell/']
    resDflanding.loc[len(resDflanding.index)] = ['GM12878','gm12878','https://www.illumina.com/platinumgenomes.html','EGRET','netZooR','https://github.com/netZoo/netZooR/releases','0.9'
        ,'https://granddb.s3.us-east-2.amazonaws.com/data/EGRET_GM12878.csv','https://granddb.s3.us-east-2.amazonaws.com/cells/ppi/EGRET_ppi.txt','http://string90.embl.de/','https://granddb.s3.us-east-2.amazonaws.com/cells/motif/EGRET_motif_prior.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/expression/LCL_expression.csv','https://www.gtexportal.org/home/datasets',687,22936,'https://genome.cshlp.org/content/32/3/524.short',130,'#cardtissue','https://github.com/netZoo/netbooks/blob/main/netbooks/netZooR/egret_banovich_netbook.ipynb','GTEx','TF','Weighill et al. (2022)','https://granddb.s3.us-east-2.amazonaws.com/cells/genotype/NA12878.vcf','https://granddb.s3.us-east-2.amazonaws.com/cells/qbic/qbic_eQTLS_GM12878_K562_finalEGRET_v1_06302020_allModels_smart1.txt','https://granddb.s3.us-east-2.amazonaws.com/cells/eqtl/eQTL_in_motif_promotor_adjacent_egene_finalEGRET_v1_06172020.txt','GM12878','https://www.gtexportal.org/home/datasets','/networks/aggregate/EGRET_GM12878_Cell/']
    resDflanding['motifDesc']= 'Motif'
    resDflanding['awsname']  = resDflanding['cardref']
    resDflanding['refs3']    = resDflanding['refs2']
    # Save dataframe
    resDflanding.to_csv('granddb/data/celllanding.csv',index=False)
    return

# save cell landing
saveCellLanding(uniquedisease, newValid)

# misc code
d = {'TF': ['TF'], 'tar': [1]}
tftarscore = pd.DataFrame(data=d)

a=pd.read_csv('/Users/mab8354/Downloads/PANDA_ACC.csv',index_col=0)
b=pd.read_csv('/Users/mab8354/Downloads/Adipose_Subcutaneous.csv',index_col=0)
c=a-b
intergenes = np.intersect1d(a.columns,b.columns)
c=c[intergenes]
