import pandas as pd
import os
from indigo import *
from indigo_renderer import *

generateIndigo=1#to be launched inside indigo folder
if generateIndigo==1:
    indigo = Indigo()
    renderer = IndigoRenderer(indigo)
    drugDf = pd.read_csv('/Users/mab8354/granddb/src/clueReg/data/drugNamesAug.csv')

    dNames = []
    for i in range(len(drugDf)):
       # 1. draw molecule using indigp
       print(drugDf['0'][i])
       print("/" in drugDf['0'][i])
       if "/" in drugDf['0'][i]:
            drugDf['0'][i] = drugDf['0'][i].replace("/", "")
       try:
            indigo.setOption("render-coloring", 1)
            m = indigo.loadMolecule(drugDf.canonical_smiles[i])
            indigo.setOption("render-stereo-style", 'none')
            renderer.renderToFile(m, '/Users/mab8354/granddb/static/molcluereg/' + drugDf['0'][i] + '.svg')
       except:
            print('structure generation failed')

    print('Fin!')
    print(dNames)


    drugDF = pd.read_csv('/Users/mab8354/granddb/src/cluereg/data/drugNamesAug.csv', header=0,index_col=0)
    drugNames = drugDF.iloc[:,0]







