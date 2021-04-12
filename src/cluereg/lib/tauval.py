import pandas as pd
import numpy as np
import os
import scipy as sp # for sparse matrices
import scipy.sparse
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import inv
import requests
import random

#os.chdir('/Users/mab8354/granddb/')

def enrichCmapReg(sampleGenesUp,sampleGenesDown,brd,sparse_matrix,genNames):
    print('Reading drug database')
    #drugDF = pd.read_csv('src/clueReg/data/drugNamesAug.csv', header=0,index_col=0)
    drugDF = pd.read_csv('data/drugNamesAug.csv', header=0, index_col=0)
    drugNames = drugDF.iloc[:,0]
    print(str(len(sampleGenesUp)) + ' Genes are Up')
    print(str(len(sampleGenesDown)) + ' Genes are Down')
    # Construct input vector
    print('Computing enrichment score to ' + str(len(drugNames)) + ' drugs')
    intersectUp     = np.array(np.in1d(genNames,sampleGenesUp) ,dtype=int)
    intersectDown   = np.array(np.in1d(genNames,sampleGenesDown),dtype=int)
    intersectUpOv   = np.concatenate([intersectUp, intersectUp])
    intersectDownOv = np.concatenate([intersectDown, intersectDown])
    # Compute overlap
    overlap         = intersectDownOv * sparse_matrix -intersectUpOv * sparse_matrix
    # Compute cosine similarity
    inputSig = intersectUp-intersectDown
    if gene==1:
        sparse_matrix_combined = sparse_matrix[:12282,:] + sparse_matrix[12282:,:]
    elif gene==0:
        sparse_matrix_combined = sparse_matrix[:644, :] + sparse_matrix[644:, :]
    cosDist  = cosine_similarity(inputSig.reshape(1,-1), sparse_matrix_combined.transpose())
    cosDist  = cosDist.transpose()
    cosDist  = np.concatenate( cosDist, axis=0 )
    # print results
    indSort  = np.argsort(cosDist)
	# stats about query
    stat1=len(sampleGenesUp)
    stat2=len(sampleGenesDown)
    stat3=np.count_nonzero(intersectUp)
    stat4=np.count_nonzero(intersectDown)
    if brd=='on':
        indBrd=[False if d[0:4]=='BRD-' else True for d in drugNames]
        drugNames= drugNames[indBrd]
        drugNames.index=list(range(0,len(drugNames)))
        cosDist  = cosDist[indBrd]
        overlap  = overlap[indBrd]
        indSort  = np.argsort(overlap)
        drugDF   = drugDF.iloc[indBrd]
    return drugNames, cosDist, overlap, indSort, stat1, stat2, stat3, stat4, drugDF


brd  = 'off' # all drugs

### Now GENES reduce size of random sets 50-500
gene = 1 # genes
random.seed(1619)
if gene==1:
    sparse_matrix = scipy.sparse.load_npz('data/sparse_cmapreg.npz')
    #sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapreg.npz')
elif gene==0:
    sparse_matrix = scipy.sparse.load_npz('data/sparse_cmapregtf.npz')
    #sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapregtf.npz')
if gene==1:
    genNames  = pd.read_csv('data/geneNames.csv',header=None) #'geneNames.csv'
    #genNames  = pd.read_csv('src/clueReg/data/geneNames.csv',header=None) #'geneNames.csv'
elif gene==0:
    genNames    = pd.read_csv('data/tfNames.csv',header=None) #'geneNames.csv'
    #genNames    = pd.read_csv('src/clueReg/data/tfNames.csv',header=None) #'geneNames.csv'

# dry run
dense_matrix=sparse_matrix.todense()


a=np.where(dense_matrix[:,0] == -1)
b=np.where(dense_matrix[:,0] == 1)
sampleGenesUp   =  genNames.iloc[b[0]]
sampleGenesDown = genNames.iloc[a[0]-12282]
drugNames, cosDist, overlap, indSort, stat1, stat2, stat3, stat4, drugDF = \
    enrichCmapReg(sampleGenesUp, sampleGenesDown, brd, sparse_matrix, genNames)

# init resdf
ndrugs= len(drugNames)
datazeros  = np.zeros((ndrugs,ndrugs))
resDfGene = pd.DataFrame(data=datazeros, index=drugNames)

for i in range(ndrugs):
    i
    # pick gene set size
    a = np.where(dense_matrix[:, i] == -1)
    b = np.where(dense_matrix[:, i] == 1)
    sampleGenesUp   = genNames.iloc[b[0]]
    sampleGenesDown = genNames.iloc[a[0] - 12282]
    drugNames, cosDist, overlap, indSort, stat1, stat2, stat3, stat4, drugDF = \
        enrichCmapReg(sampleGenesUp,sampleGenesDown,brd,sparse_matrix,genNames)
    #ordered from lowest cosine
    resDfGene.iloc[:,i]=cosDist

# order dataframe by index
a = resDfGene.values
a.sort(axis=1)  # no ascending argument
resDfGene = pd.DataFrame(a, resDfGene.index, resDfGene.columns)

resDfGene.to_csv('resDfGeneTau.csv')


### Now TFs reduce size of random sets 50-500
gene = 0 # tfs
random.seed(1619)
if gene==1:
    sparse_matrix = scipy.sparse.load_npz('data/sparse_cmapreg.npz')
    #sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapreg.npz')
elif gene==0:
    sparse_matrix = scipy.sparse.load_npz('data/sparse_cmapregtf.npz')
    #sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapregtf.npz')
if gene==1:
    genNames  = pd.read_csv('data/geneNames.csv',header=None) #'geneNames.csv'
    #genNames  = pd.read_csv('src/clueReg/data/geneNames.csv',header=None) #'geneNames.csv'
elif gene==0:
    genNames    = pd.read_csv('data/tfNames.csv',header=None) #'geneNames.csv'
    #genNames    = pd.read_csv('src/clueReg/data/tfNames.csv',header=None) #'geneNames.csv'

# dry run
dense_matrix=sparse_matrix.todense()


a=np.where(dense_matrix[:,0] == -1)
b=np.where(dense_matrix[:,0] == 1)
sampleGenesUp   =  genNames.iloc[b[0]]
sampleGenesDown = genNames.iloc[a[0]-644]
drugNames, cosDist, overlap, indSort, stat1, stat2, stat3, stat4, drugDF = \
    enrichCmapReg(sampleGenesUp, sampleGenesDown, brd, sparse_matrix, genNames)

# init resdf
ndrugs= len(drugNames)
datazeros  = np.zeros((ndrugs,ndrugs))
resDfGene = pd.DataFrame(data=datazeros, index=drugNames)

for i in range(ndrugs):
    i
    # pick gene set size
    a = np.where(dense_matrix[:, i] == -1)
    b = np.where(dense_matrix[:, i] == 1)
    sampleGenesUp   = genNames.iloc[b[0]]
    sampleGenesDown = genNames.iloc[a[0] - 644]
    drugNames, cosDist, overlap, indSort, stat1, stat2, stat3, stat4, drugDF = \
        enrichCmapReg(sampleGenesUp,sampleGenesDown,brd,sparse_matrix,genNames)
    #ordered from lowest cosine
    resDfGene.iloc[:,i]=cosDist

# order dataframe by index
a = resDfGene.values
a.sort(axis=1)  # no ascending argument
resDfGene = pd.DataFrame(a, resDfGene.index, resDfGene.columns)

resDfGene.to_csv('resDfTFTau.csv')


aws s3 cp s3://cmapreg/temp/drugNamesAug.csv .
aws s3 cp s3://cmapreg/temp/geneNames.csv .
aws s3 cp s3://cmapreg/temp/tfNames.csv .
aws s3 cp s3://cmapreg/temp/sparse_cmapreg.npz .
aws s3 cp s3://cmapreg/temp/sparse_cmapregtf.npz .
aws s3 cp s3://cmapreg/temp/hgnc_complete_set.txt .
