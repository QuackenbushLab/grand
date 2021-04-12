import pandas as pd

os.chdir('/Users/mab8354/granddb/')

df=pd.read_csv('~/Downloads/GO_Biological_Process_2018.txt',sep='\t',header=None)
newdf=pd.DataFrame(columns=['term','goid','genelist'])

term,goid,genelist = [],[],[]
for i in range(df.shape[0]):
    a=df.iloc[i,0]
    b=str.split(a,')')
    term.append(str.split(b[0],'(')[0][:-1])
    goid.append(str.split(b[0],'(')[1])
    genelist.append(b[1][2:-2])


newdf['term'] = term
newdf['goid'] = goid
newdf['genelist'] = genelist

newdf.to_csv('data/gobp2018.csv')