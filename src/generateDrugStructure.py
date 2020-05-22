import pandas as pd
import os
from indigo import *
from indigo_renderer import *

generateIndigo=1#to be launched inside indigo folder
if generateIndigo==1:
    indigo = Indigo()
    renderer = IndigoRenderer(indigo)
    drugDf = pd.read_csv('/Users/mab8354/granddb/drug_desc.csv')

    dNames = []
    for i in range(len(drugDf)):
       # 1. draw molecule using indigp
       print(drugDf.pert_iname[i])
       print("/" in drugDf.pert_iname[i])
       if "/" in drugDf.pert_iname[i]:
            drugDf.pert_iname[i] = drugDf.pert_iname[i].replace("/", "")
       try:
            indigo.setOption("render-coloring", 1)
            m = indigo.loadMolecule(drugDf.smiles[i])
            indigo.setOption("render-stereo-style", 'none')
            renderer.renderToFile(m, '/Users/mab8354/granddb/static/images/' + drugDf.pert_iname[i] + '.svg')
       except:
            indigo.setOption("render-coloring", 1)
            m = indigo.loadMolecule(drugDf.canonical_smiles[i])
            indigo.setOption("render-stereo-style", 'none')
            renderer.renderToFile(m, '/Users/mab8354/granddb/static/images/' + drugDf.pert_iname[i] + '.svg')

    print('Fin!')
    print(dNames)









