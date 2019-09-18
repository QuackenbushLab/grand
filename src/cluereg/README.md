### Introduction
cluereg is a regulatory network version of the [clue.io](https://clue.io) database of drug-induced gene expression of over 20,000 small molecules.
While clue uses the gene expression to compute the connectivity between compounds, clureg infers the regulatory network for each drug using the PANDA algorithm [1] to compute the targeting score for each gene. clureg then computes a similarity metric between a user input and drug regulatory signatures.

### Usage
`python3 lib/enrichCmapReg.py data/sparse_cmapreg.npz data/geneNames.csv data/drugNames.csv data/sampleUp.csv data/sampleDown.csv`

+ sparse_cmapreg.npz: drug differential targeting database

+ geneNames.csv: gene names database

+ drugNames.csv: drug names database

+ sampleUp.csv: list of genes up-regulated, to be replaced with user input

+ sampleDown.csv: list of genes down-regulated, ot be replaced with user input

### Results
The script will output sorted drug results in `results.csv`

#### Scores
The overlap score [2] in `results.csv` is intersect(Input_Genes_Up,Drug_Genes_down) + intersect(Input_Genes_Down,Drug_Genes_Up) - intersect(Input_Genes_Up,Drugs_Genes_Up) - intersect(Input_Genes_Down,Drugs_Genes_Down)

The cosine similarity [3] compares the input vector to all the drugs. It is a signed measures that measures the direction of the vectors rather than their amplitude. In our case, we are interested in measuring the vectors of opposite directions, thus having negative cosine similarity.

### Dependencies
Requires scipy, numpy, sklearn, and pandas.

### References
[1] Glass, Kimberly, et al. "Passing messages between biological networks to refine predicted interactions." PloS one 8.5 (2013): e64832.

[2] Zhong, Yifei, et al. "Renoprotective effect of combined inhibition of angiotensin-converting enzyme and histone deacetylase." Journal of the American Society of Nephrology 24.5 (2013): 801-811.

[3] Duan, Qiaonan, et al. "L1000CDS 2: LINCS L1000 characteristic direction signatures search engine." NPJ systems biology and applications 2 (2016): 16015.
