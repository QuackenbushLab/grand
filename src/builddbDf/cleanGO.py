import pandas as pd

os.chdir('/Users/mab8354/granddb/')

df=pd.read_csv('data/GO_Biological_Process_2018.txt',sep='\t',header=None)
newdf=pd.DataFrame(columns=['term','goid','genelist'])

term,goid,genelist = [],[],[]
for i in range(df.shape[0]):
    a=df.iloc[i,0]
    b=str.split(a,')')
    if len(b)>2:
        term.append( ')'.join([b[0], str.split(b[1],'(')[0][:-1] ]) )
        goid.append(str.split(b[1],'(')[1])
        genelist.append(b[2][2:-2])
    else:
        term.append(str.split(b[0],'(')[0][:-1])
        goid.append(str.split(b[0],'(')[1])
        genelist.append(b[1][2:-2])

newdf['term'] = term
newdf['goid'] = goid
newdf['genelist'] = genelist

newdf.to_csv('data/gobp2018.csv')

# 2. reverse GO
megagenelist=[]
for i in range(len(genelist)):
    megagenelist.extend(str.split(genelist[i],','))
megagenelist=np.unique(megagenelist)
# build matrix
revDf = pd.DataFrame(data=np.zeros((len(megagenelist),1)),index=megagenelist, columns=['terms'])
revDf['terms']=''
for i in range(df.shape[0]):
    a=df.iloc[i,0]
    b=str.split(a,')')
    if len(b)>2:
        term = ')'.join([b[0], str.split(b[1],'(')[0][:-1] ])
        genelist = str.split(b[2][2:-2],',')
    else:
        term= str.split(b[0],'(')[0][:-1]
        genelist = str.split(b[1][2:-2],',')
    revDf.loc[genelist]=revDf.loc[genelist]+'\n'+term

# remove empty gene
revDf = revDf.drop('',axis=0)
revDf.to_csv('data/gobp2018bygene.csv')


# II. now GWAS catalog
os.chdir('/Users/mab8354/granddb/')

df=pd.read_csv('data/GWAS_Catalog_2019.txt',sep='\t',header=None)
newdf=pd.DataFrame(columns=['term','genelist'])

term,genelist = [],[]
for i in range(df.shape[0]):
    a = df.iloc[i, 0]
    b = str.split(a, ',')
    empind=np.where(np.in1d(b,''))[0][0]
    if empind > 1:
        term.append( ''.join(b[0:empind]) )
        genelist.append(','.join(b[(empind+1):-1]))
    else:
        term.append( b[0] )
        genelist.append(','.join(b[2:-1]))

newdf['term'] = term
newdf['genelist'] = genelist

newdf.to_csv('data/gwascata.csv')

# 2. reverse Gwas catalog
megagenelist=[]
for i in range(len(genelist)):
    megagenelist.extend(str.split(genelist[i],','))
megagenelist=np.unique(megagenelist)
# build matrix
revDfgwas = pd.DataFrame(data=np.zeros((len(megagenelist),1)),index=megagenelist, columns=['terms'])
revDfgwas['terms']=''
for i in range(df.shape[0]):
    a = df.iloc[i, 0]
    b = str.split(a, ',')
    empind=np.where(np.in1d(b,''))[0][0]
    if empind > 1:
        term = ''.join(b[0:empind])
        genelist = b[(empind+1):-1]
    else:
        term= b[0]
        genelist=b[2:-1]
    revDfgwas.loc[genelist] = revDfgwas.loc[genelist] + '\n' + term

# remove empty gene
revDfgwas.to_csv('data/gwascatabygene.csv')
