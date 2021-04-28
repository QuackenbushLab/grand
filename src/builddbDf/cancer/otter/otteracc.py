import pandas as pd

os.chdir('/Users/mab8354/')


indexNames=['COR','PARTIAL-COR','ARACNE','GENIE3','TIGRESS','OTTER-SPECTRAL','GRAMPA-GRAD','QAP-GRAD','OTTER-GRAD','PANDA',\
            'OTTER-SPECTRAL*','GRAMPA-GRAD*','QAP-GRAD*','OTTER-GRAD*','PANDA*']

 a=[[0.5857, 0.5692, 0.5785, 0.2774, 0.2219, 0.3094],
 [0.5366, 0.5209, 0.5175, 0.2361, 0.1952, 0.2525],
 [0.6150, 0.5234, 0.5636, 0.2858, 0.2027, 0.2986],
 [0.4818, 0.4832, 0.4846, 0.2064, 0.1836, 0.2437],
 [0.4945, 0.4808, 0.5018, 0.2088, 0.1845, 0.2523],
 [0.5787, 0.5420, 0.5345, 0.2555, 0.2024, 0.2614],
 [0.6000, 0.5896, 0.5670, 0.2729, 0.2214, 0.2796],
 [0.5722, 0.6031, 0.5335, 0.2526, 0.2346, 0.2587],
 [0.6936, 0.6826, 0.6477, 0.3752, 0.3176, 0.3717],
 [0.6739, 0.6642, 0.6211, 0.3481, 0.2960, 0.3503],
 [0.6123, 0.6070, 0.5973, 0.2773, 0.2367, 0.3183],
 [0.6312, 0.6312, 0.6021, 0.3150, 0.2551, 0.3098],
 [0.7114, 0.7096, 0.6883, 0.3568, 0.3216, 0.3764],
 [0.7161, 0.7215, 0.7166, 0.3574, 0.3280, 0.4063],
 [0.7008, 0.6642, 0.6180, 0.3497, 0.2676, 0.3340]]

df=pd.DataFrame(columns=['aurocbr','auroccer','aurocliv','auprbr','auprcer','auprliv'],data=np.array(a),index=indexNames)
df.to_csv('granddb/data/otteracc.csv')

# PANDA accuracy
b=[[0.727,0.719,0.718],
[0.706,0.704,0.718],
[0.685,0.544,0.675],
[0.504,0.551,0.539],
[0.503,0.502,0.500]]


indexNames=['PANDA','SEREND','ReMoDiscovery','CLR','C3Net']
df2=pd.DataFrame(columns=['ko','cc','sr'],data=np.array(b),index=indexNames)
df2.to_csv('granddb/data/pandaacc.csv')


# DRAGON accuracy

c=[[0.52,0.5],
   [0.57,0.52],
   [0.72,0.65],
   [0.84,0.83],
   [0.883,0.878],
   [0.913,0.91]]


indexNames=['400','800','1200','1600','2000','2400']
df3=pd.DataFrame(columns=['dragon','ggm'],data=np.array(c),index=indexNames)
df3.to_csv('granddb/data/dragonacc.csv')











