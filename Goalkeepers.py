
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt



cols_to_remove = ['Rk','Player','Nation','Pos','Squad','Comp','Age','Born','90s']

gk=pd.read_excel('Goalkeeping.xlsx').drop(['Rk','MP','Starts'],axis=1)
advancedgk=pd.read_excel('AdvanceGoalkeeping.xlsx').drop(cols_to_remove,axis=1)
pd.set_option('display.max_columns',None)




def renamecols(table_no,data):
    no=str(table_no) + '_'
    return data.rename(columns = lambda x: no+x)
advancedgk=renamecols(2,advancedgk)

grand=pd.concat([gk,advancedgk],axis=1)



GK=grand[grand['Min']>=500].reset_index()
GK.head()



GK['Comp']=GK['Comp'].str.split(' ',expand=True,n=1)[1]
GK['Nation']=GK['Nation'].str.split(' ',expand=True,n=1)[1]
GK=GK[GK['Pos']=='GK'].reset_index()
GK=GK.fillna(0)



Gk_unique=[]

for i in range(len(GK)):
    Gk_unique.append(GK['Player'][i] +' ({})'.format(GK['Squad'][i]))

Goalkeeper_ID=dict(zip(Gk_unique,np.arange(len(Gk_unique))))  
Goalkeeper_ID


print(len(GK))

#
#
# with open(r'pickle\Goalkeeper_ID.pickle', 'wb') as file:
#     pickle.dump(Goalkeeper_ID, file)
#
#
# GK=GK.drop(['level_0','index'],axis=1)
#
#
# with open('GK.pickle', 'wb') as file:
#     pickle.dump(GK, file)
#
#
#
#
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
#
# statsgk=GK.iloc[:,9:]
# datagk=StandardScaler().fit_transform(statsgk)
#
#
#
#
#
# datagk.shape
#
#
# PCAgk=PCA()
# PCAgk.n_components=40
# pcagk_data=PCAgk.fit_transform(datagk)
#
# per_var=PCAgk.explained_variance_/np.sum(PCAgk.explained_variance_)
# cum_variance=np.cumsum(per_var)
#
#
# plt.figure(1, figsize=(12, 6))
# plt.plot(cum_variance, linewidth=2)
# plt.axis('tight')
# plt.grid()
# plt.xlabel('principal components')
# plt.ylabel('Cumulative variance explained')
# plt.title('PCA: components selection')
#
#
# from scipy.spatial import distance
# from tqdm import tqdm
#
#
# statsgk=pcagk_data[:,:]
#
# def getStatsGk(name):
#     index=Goalkeeper_ID[name]
#     return statsgk[index,:]
#
# def similiarity(player1,player2):
#     return 1 - distance.cosine(getStatsGk(player1), getStatsGk(player2))
#
# def normalize(array):
#     return np.array([round(num, 2) for num in (array - min(array))*100/(max(array)-min(array))])
#
#
#
# engine_gk = {}
# for query in tqdm(Gk_unique):
#     metric_gk = []
#     for player in Gk_unique:
#         value =similiarity(query,player)
#         metric_gk.append(value)
#     metric_gk = normalize(metric_gk)
#     engine_gk[query] = metric_gk
#
#
# with open(r'pickle\engine_gk.pickle', 'wb') as file:
#     pickle.dump(engine_gk, file)
#





