import pandas as pd
import numpy as np
import os
import scipy as sp # for sparse matrices
import scipy.sparse
import sys # for arguments
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import inv
import requests

#os.chdir('/Users/mab8354/cluereg/')

# Read database
print('Reading drug database')
#db         = pd.read_csv('cmapreg.csv', header=None,dtype=np.float64)
#sparse_matrix = scipy.sparse.load_npz('data/sparse_cmapreg.npz')
sparse_matrix = scipy.sparse.load_npz(sys.argv[1]) #('sparse_cmapreg.npz')
# None of python's sparse libraries allow storing colnames and rownames so they have to be maintained separetaly
#geneNames  = pd.read_csv('data/geneNames.csv',header=None) #'geneNames.csv'
#drugNames  = pd.read_csv('data/drugNames.csv',header=None) #'drugNames.csv'
geneNames  = pd.read_csv(sys.argv[2],header=None) #'geneNames.csv'
drugNames  = pd.read_csv(sys.argv[3],header=None) #'drugNames.csv'
#db.columns = drugNames
#geneNames  = geneNames.append(geneNames)

# Save to sparse
#sparse_matrix = sp.sparse.csc_matrix(db)
#sp.sparse.save_npz('sparse_cmapreg.npz', sparse_matrix)

# Read genes
print('Reading input gene list ')
#sampleGenesUp  = pd.read_csv('data/sampleUp.csv',header=None,dtype=str) #'sampleUp.csv'
#sampleGenesDown= pd.read_csv('data/sampleDown.csv',header=None,dtype=str) #'sampleDown.csv'
sampleGenesUp  = pd.read_csv(sys.argv[4],header=None,dtype=str) #'sampleUp.csv'
sampleGenesDown= pd.read_csv(sys.argv[5],header=None,dtype=str) #'sampleDown.csv'
print(str(len(sampleGenesUp)) + ' Genes are Up')
print(str(len(sampleGenesDown)) + ' Genes are Down')

# Construct input vector
print('Computing enrichment score to ' + str(len(drugNames)) + ' drugs')
intersectUp     = np.array(np.in1d(geneNames,sampleGenesUp) ,dtype=int)
intersectDown   = np.array(np.in1d(geneNames,sampleGenesDown),dtype=int)
intersectUpOv   = np.concatenate([intersectUp, intersectUp])
intersectDownOv = np.concatenate([intersectDown, intersectDown])

# Compute overlap
overlap         = intersectDownOv * sparse_matrix -intersectUpOv * sparse_matrix

# Compute cosine similarity
inputSig = intersectUp-intersectDown
sparse_matrix_combined = sparse_matrix[:12282,:] + sparse_matrix[12282:,:]
cosDist  = cosine_similarity(inputSig.reshape(1,-1), sparse_matrix_combined.transpose())
cosDist  = cosDist.transpose()
cosDist  = np.concatenate( cosDist, axis=0 )

# print results
indSort  = np.argsort(overlap)
d = {'overlapScore': overlap[list(reversed(indSort))], 'cosine similarity': cosDist[list(reversed(indSort))] }
res = pd.DataFrame(data=d)
res.index = drugNames.iloc[list(reversed(indSort))]
#res.to_csv('results.csv')

#print('Results written to results.csv')

# post to API
max_display = 100
for i in range(max_display):
	payload = {'drug':drugNames.iloc[indSort[i]],'cosine':round(cosDist[indSort[i]],4),'overlap':overlap[indSort[i]]}
	r = requests.put('http://localhost:8000/api/v1/drugresultup/' + str(i+1) + '/', data=payload)
	#print(r.status_code)

for i in range(max_display):
        payload = {'drug':drugNames.iloc[indSort[-1-i]],'cosine':round(cosDist[indSort[-1-i]],4),'overlap':overlap[indSort[-1-i]]}
        r = requests.put('http://localhost:8000/api/v1/drugresultdown/' + str(i+1) + '/', data=payload)
        #print(r.status_code)

# stats about query
payload = {'genesupin': len(sampleGenesUp),'genesdownin':len(sampleGenesDown),'genesup':np.count_nonzero(intersectUp),'genesdown':np.count_nonzero(intersectDown)}
r = requests.put('http://localhost:8000/api/v1/params/0/', data=payload)
