import pandas as pd
import numpy as np
import os
import scipy as sp # for sparse matrices
import scipy.sparse
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import inv
import requests
import random

os.chdir('/Users/mab8354/granddb/')

def enrichCmapReg(gene,sampleGenesUp,sampleGenesDown,brd):
    print('Reading drug database')
    #db         = pd.read_csv('cmapreg.csv', header=None,dtype=np.float64)
    if gene==1:
	    sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapreg.npz')
    elif gene==0:
        sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapregtf.npz')

	#sparse_matrix = scipy.sparse.load_npz(sys.argv[1]) #('sparse_cmapreg.npz')
	# None of python's sparse libraries allow storing colnames and rownames so they have to be maintained separetaly
    if gene==1:
        genNames  = pd.read_csv('src/clueReg/data/geneNames.csv',header=None) #'geneNames.csv'
    elif gene==0:
        genNames    = pd.read_csv('src/clueReg/data/tfNames.csv',header=None) #'geneNames.csv'
    drugDF = pd.read_csv('src/clueReg/data/drugNamesAug.csv', header=0,index_col=0)
    drugNames = drugDF.iloc[:,0]
    #drugNames  = pd.read_csv('src/cluereg/data/drugNames.csv',header=None)
    #geneNames  = pd.read_csv(sys.argv[2],header=None) #'geneNames.csv'
    #drugNames  = pd.read_csv(sys.argv[3],header=None) #'drugNames.csv'
    #db.columns = drugNames
    #geneNames  = geneNames.append(geneNames)

	# Save to sparse
	#sparse_matrix = sp.sparse.csc_matrix(db)
	#sp.sparse.save_npz('sparse_cmapreg.npz', sparse_matrix)

    # Read genes
    #sampleGenesUp  = pd.read_csv('src/cluereg/data/sampleUp.csv',header=None,dtype=str) #'sampleUp.csv'
    #sampleGenesDown= pd.read_csv('src/cluereg/data/sampleDown.csv',header=None,dtype=str) #'sampleDown.csv'
    #sampleGenesUp  = pd.read_csv(sys.argv[4],header=None,dtype=str) #'sampleUp.csv'
	#sampleGenesDown= pd.read_csv(sys.argv[5],header=None,dtype=str) #'sampleDown.csv'
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
    indSort  = np.argsort(overlap)
    #d = {'overlapScore': overlap[list(reversed(indSort))], 'cosine similarity': cosDist[list(reversed(indSort))] }
    #res = pd.DataFrame(data=d)
    #res.index = drugNames.iloc[list(reversed(indSort))]
    #res.to_csv('results.csv')

    #print('Results written to results.csv')

	# post to API
	#max_display = 100
	#for i in range(max_display):
		#payload = {'drug':drugNames.iloc[indSort[i]],'cosine':round(cosDist[indSort[i]],4),'overlap':overlap[indSort[i]]}
		#r = requests.put('http://localhost:8000/api/v1/drugresultup/' + str(i+1) + '/', data=payload)
		#print(r.status_code)

	#for i in range(max_display):
	        #payload = {'drug':drugNames.iloc[indSort[-1-i]],'cosine':round(cosDist[indSort[-1-i]],4),'overlap':overlap[indSort[-1-i]]}
	        #r = requests.put('http://localhost:8000/api/v1/drugresultdown/' + str(i+1) + '/', data=payload)
	        #print(r.status_code)

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


gene=1
sampleGenesUp='ENSG00000137154\nENSG00000160049\nENSG00000281221\nENSG00000137822\nENSG00000113739\nENSG00000139146\nENSG00000099721\nENSG00000147488\nENSG00000116824\nENSG00000013583\nENSG00000105671\nENSG00000012983\nENSG00000013288\nENSG00000102871\nENSG00000226248\nENSG00000102226\nENSG00000136856\nENSG00000108312\nENSG00000132591\nENSG00000175895\nENSG00000198353\nENSG00000130005\nENSG00000177548\nENSG00000110171\nENSG00000026559\nENSG00000170345\nENSG00000173638\nENSG00000125730\nENSG00000198000\nENSG00000125931\nENSG00000176387\nENSG00000232860\nENSG00000229937\nENSG00000197475\nENSG00000135346\nENSG00000213931\nENSG00000030419\nENSG00000156802\nENSG00000146842\nENSG00000196655\nENSG00000110944\nENSG00000228435\nENSG00000156222\nENSG00000146143\nENSG00000177595\nENSG00000019582\nENSG00000160959\nENSG00000185958\nENSG00000256771\nENSG00000139874\nENSG00000116745\nENSG00000140092\nENSG00000120235\nENSG00000128285\nENSG00000156049\nENSG00000157782\nENSG00000168229\nENSG00000111012\nENSG00000170852\nENSG00000147437\nENSG00000088543\nENSG00000108953\nENSG00000125843\nENSG00000170950\nENSG00000148943\nENSG00000124549\nENSG00000196591\nENSG00000169242\nENSG00000175426\nENSG00000105339\nENSG00000163605\nENSG00000132677\nENSG00000134538\nENSG00000158874\nENSG00000085185\nENSG00000135116\nENSG00000168268\nENSG00000102100\nENSG00000172215\nENSG00000165494\nENSG00000198417\nENSG00000102003\nENSG00000169764\nENSG00000057294\nENSG00000167548\nENSG00000183242\nENSG00000116711\nENSG00000100307\nENSG00000103126\nENSG00000137673\nENSG00000116106\nENSG00000111640\nENSG00000174483\nENSG00000073331\nENSG00000110169\nENSG00000250254\nENSG00000163737\nENSG00000204248\nENSG00000198650\nENSG00000125826\n'
sampleGenesDown='ENSG00000127528\nENSG00000165487\nENSG00000160181\nENSG00000158815\nENSG00000136932\nENSG00000254997\nENSG00000107104\nENSG00000104881\nENSG00000182326\nENSG00000084093\nENSG00000165792\nENSG00000077498\nENSG00000085788\nENSG00000184302\nENSG00000108861\nENSG00000165280\nENSG00000178445\nENSG00000196372\nENSG00000181143\nENSG00000127125\nENSG00000182446\nENSG00000198056\nENSG00000062485\nENSG00000146276\nENSG00000067064\nENSG00000077380\nENSG00000163946\nENSG00000122299\nENSG00000183549\nENSG00000174483\nENSG00000076382\nENSG00000111716\nENSG00000139718\nENSG00000131747\nENSG00000164035\nENSG00000095319\nENSG00000164081\nENSG00000170075\nENSG00000178053\nENSG00000179477\nENSG00000163624\nENSG00000134243\nENSG00000072682\nENSG00000214022\nENSG00000124783\nENSG00000100941\nENSG00000152402\nENSG00000119655\nENSG00000111450\nENSG00000164128\nENSG00000147804\nENSG00000278548\nENSG00000146834\nENSG00000134684\nENSG00000092345\nENSG00000253293\nENSG00000088726\nENSG00000111328\nENSG00000145244\nENSG00000196646\nENSG00000036549\nENSG00000125726\nENSG00000080709\nENSG00000011295\nENSG00000010256\nENSG00000198815\nENSG00000066044\nENSG00000089154\nENSG00000179455\nENSG00000095752\nENSG00000142657\nENSG00000253729\nENSG00000133740\nENSG00000105229\nENSG00000059145\nENSG00000100342\nENSG00000114742\nENSG00000103187\nENSG00000103174\nENSG00000111145\nENSG00000070366\nENSG00000196954\nENSG00000025156\nENSG00000105997\nENSG00000183648\nENSG00000157150\nENSG00000166167\nENSG00000163754\nENSG00000147457\nENSG00000083896\nENSG00000078142\nENSG00000084112\nENSG00000041357\nENSG00000127948\nENSG00000078403\nENSG00000242372\nENSG00000206073\nENSG00000103994\nENSG00000163739\nENSG00000114867\n'
data = sampleGenesUp.split('\n')
dataup = list(filter(None, data))
data = sampleGenesDown.split('\n')
datadown = list(filter(None, data))
brd='off'

drugNames, cosDist, overlap, indSort, stat1, stat2, stat3, stat4, drugDF=enrichCmapReg(gene,dataup,datadown,brd)

overlap=overlap[indSort]
cosDist=cosDist[indSort]
drugNames=drugNames[indSort]

# compute combinations
topdrugs=50
drugNames = drugNames[0:topdrugs]
cosDist   = cosDist[0:topdrugs]
overlap   = overlap[0:topdrugs]
indSort   = indSort[0:topdrugs]

if gene==1:
	sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapreg.npz')
elif gene==0:
    sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapregtf.npz')


if gene==1:
    sparse_matrix_combined = sparse_matrix[:12282,:] + sparse_matrix[12282:,:]
elif gene==0:
    sparse_matrix_combined = sparse_matrix[:644, :] + sparse_matrix[644:, :]

dense_matrix_combined=sparse_matrix_combined.todense()
dense_matrix_combined_sel=dense_matrix_combined[:,indSort]


colNames,resmat=[],[]
for i in range(topdrugs-1):
    cosDist = cosine_similarity(np.transpose(dense_matrix_combined_sel[:,i]), np.transpose(dense_matrix_combined_sel[:,i+1:]))
    resmat = np.concatenate((resmat,cosDist.flatten()))

newcols=[]
for i in range(topdrugs):
    for j in range(i+1,topdrugs):
        newcols.append(drugNames.iloc[i] + '_' + drugNames.iloc[j])

resdf=pd.DataFrame(data=resmat, columns=['cosine'], index=newcols)




## Check cosine

drugDF = pd.read_csv('src/clueReg/data/drugNamesAug.csv', header=0,index_col=1)
n1=drugDF.loc['DASB'][0]
n2=drugDF.loc['avrainvillamide-analog-2'][0]

# on genes
sparse_matrix = scipy.sparse.load_npz('src/clueReg/data/sparse_cmapregtf.npz')
sparse_matrix_combined = sparse_matrix[:644,:] + sparse_matrix[644:,:]

cosDist = cosine_similarity(sparse_matrix_combined[:,n1].transpose(), sparse_matrix_combined[:,n2].transpose())