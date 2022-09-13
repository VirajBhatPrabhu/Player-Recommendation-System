#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import numpy as np





cols_to_remove = ['Rk','Player','Nation','Pos','Squad','Comp','Age','Born','90s']

Defense=pd.read_excel('Defense.xlsx').drop(cols_to_remove,axis=1)
Gca=pd.read_excel('Goal-shotcreation.xlsx').drop(cols_to_remove,axis=1)
Passtypes=pd.read_excel('Passtype.xlsx').drop(cols_to_remove,axis=1)
Possession=pd.read_excel('Posession.xlsx').drop(cols_to_remove,axis=1)
Shooting=pd.read_excel('Shoot.xlsx').drop(cols_to_remove,axis=1)
Misc=pd.read_excel('miscallaneous.xlsx').drop(cols_to_remove,axis=1)
Passing=pd.read_excel('passing.xlsx').drop(cols_to_remove,axis=1)
standard=pd.read_excel('Standard.xlsx').drop(['Rk','MP','Starts'],axis=1)


# In[ ]:


pd.set_option('display.max_columns',None)
standard.head(2)


# #### Lets make separate dataframes for each Mid, Def and Att

# In[ ]:


def renamecols(table_no,data):
    no=str(table_no) + '_'
    return data.rename(columns = lambda x: no+x)


Defense=renamecols(5,Defense)
Gca=renamecols(7,Gca)
Passtypes=renamecols(3,Passtypes)
Possession=renamecols(4,Possession)
Shooting=renamecols(6,Shooting)
Misc=renamecols(8,Misc)
Passing=renamecols(2,Passing)


Midieldfinal_table=pd.concat([standard,Passing,Passtypes,Possession,Defense,Shooting,Gca,Misc],axis=1)


# In[ ]:


def renamecols(table_no,data):
    no=str(table_no) + '_'
    return data.rename(columns = lambda x: no+x)


Defense=renamecols(8,Defense)
Gca=renamecols(3,Gca)
Passtypes=renamecols(5,Passtypes)
Possession=renamecols(6,Possession)
Shooting=renamecols(2,Shooting)
Misc=renamecols(7,Misc)
Passing=renamecols(4,Passing)


Forwadfinal_table=pd.concat([standard,Shooting,Gca,Passing,Passtypes,Possession,Misc,Defense],axis=1)


# In[ ]:


def renamecols(table_no,data):
    no=str(table_no) + '_'
    return data.rename(columns = lambda x: no+x)


Defense=renamecols(2,Defense)
Gca=renamecols(8,Gca)
Passtypes=renamecols(5,Passtypes)
Possession=renamecols(4,Possession)
Shooting=renamecols(6,Shooting)
Misc=renamecols(7,Misc)
Passing=renamecols(3,Passing)


Defensefinal_table=pd.concat([standard,Defense,Passing,Possession,Passtypes,Shooting,Misc,Gca],axis=1)


# .

# In[ ]:


Midieldfinal_table.head()


# In[ ]:


# mf= MF,MFFW,MFDF
# df=DF,DFMF,DFFW
# fw=FW,FWMF,FWDF


Midfielders=Midieldfinal_table[(Midieldfinal_table['Pos']=='MF')|(Midieldfinal_table['Pos']=='MFFW')|(Midieldfinal_table['Pos']=='MFDF')].reset_index()
Defenders = Defensefinal_table[(Defensefinal_table['Pos']=='DF')|(Defensefinal_table['Pos']=='DFFW')|(Defensefinal_table['Pos']=='DFMF')].reset_index()
Forwards = Forwadfinal_table[(Forwadfinal_table['Pos']=='FW')|(Forwadfinal_table['Pos']=='FWMF')|(Forwadfinal_table['Pos']=='FWDF')].reset_index()

Midfielders=Midfielders[Midfielders['Min']>=500]
Defenders=Defenders[Defenders['Min']>=500]
Forwards=Forwards[Forwards['Min']>=500]

Midfielders['Comp']=Midfielders['Comp'].str.split(' ', expand=True, n=1)[1]
Midfielders['Nation']=Midfielders['Nation'].str.split(' ', expand=True, n=1)[1]

Defenders['Comp']=Defenders['Comp'].str.split(' ', expand=True, n=1)[1]
Defenders['Nation']=Defenders['Nation'].str.split(' ', expand=True, n=1)[1]

Forwards['Comp']=Forwards['Comp'].str.split(' ', expand=True, n=1)[1]
Forwards['Nation']=Forwards['Nation'].str.split(' ', expand=True, n=1)[1]


# In[ ]:


print(Midfielders.isna().sum().sum())
print(Defenders.isna().sum().sum())
print(Forwards.isna().sum().sum())


# In[ ]:


Midfielders=Midfielders.fillna(0)
Defenders=Defenders.fillna(0)
Forwards=Forwards.fillna(0)


# In[ ]:


print(Midfielders['Player'].duplicated().sum())
print(Defenders['Player'].duplicated().sum())
print(Forwards['Player'].duplicated().sum())


# In[ ]:


Midfielders =Midfielders.reset_index()
Defenders =Defenders.reset_index()
Forwards =Forwards.reset_index()


# In[ ]:


mid_unique=[]

for i in range(len(Midfielders)):
    mid_unique.append(Midfielders['Player'][i] +' ({})'.format(Midfielders['Squad'][i]))

midfielder_ID =dict(zip(mid_unique,np.arange(len(mid_unique))))  



# In[ ]:


def_unique=[]

for i in range(len(Defenders)):
    def_unique.append(Defenders['Player'][i] +' ({})'.format(Defenders['Squad'][i]))

defender_ID =dict(zip(def_unique,np.arange(len(def_unique))))  


# In[ ]:


forw_unique=[]

for i in range(len(Forwards)):
    forw_unique.append(Forwards['Player'][i] +' ({})'.format(Forwards['Squad'][i]))

forward_ID =dict(zip(forw_unique,np.arange(len(forw_unique))))


#
# import pickle
# with open(r'pickle\midfielder_ID.pickle', 'wb') as file:
#     pickle.dump(midfielder_ID, file)
#
# with open(r'pickle\defender_ID.pickle', 'wb') as file:
#     pickle.dump(defender_ID, file)
#
# with open(r'pickle\forward_ID.pickle', 'wb') as file:
#     pickle.dump(forward_ID, file)


# In[ ]:
print(len(Midfielders))
print(len(Defenders))
print(len(Forwards))

foot = []

for i in range(len(Midfielders)):
    # ratio of left to right foot passes
    val = Midfielders['3_Left'][i]/(Midfielders['3_Right'][i])
    if val>1:
        foot.append('left')
    else:
        foot.append('right')
#
# # adding to the data frame
# Midfielders['Foot'] = foot
#
#
# # In[ ]:
#
#
# foot = []
#
# for i in range(len(Forwards)):
#     # ratio of left to right foot passes
#     val = Forwards['5_3_Left'][i]/(Forwards['5_3_Right'][i])
#     if val>1:
#         foot.append('left')
#     else:
#         foot.append('right')
#
# # adding to the data frame
# Forwards['Foot'] = foot
#
#
# # In[ ]:
#
#
# foot = []
#
# for i in range(len(Defenders)):
#     # ratio of left to right foot passes
#     val = Defenders['5_5_3_Left'][i]/(Defenders['5_5_3_Right'][i])
#     if val>1:
#         foot.append('left')
#     else:
#         foot.append('right')
#
# # adding to the data frame
# Defenders['Foot'] = foot
#
#
# # In[ ]:
#
#
# Midfielders.drop(['level_0','index'],axis=1,inplace=True)
# Forwards.drop(['level_0','index'],axis=1,inplace=True)
# Defenders.drop(['level_0','index'],axis=1,inplace=True)
#
#
# # In[ ]:
# import pickle
#
# with open('Midfielders.pickle', 'wb') as file:
#     pickle.dump(Midfielders, file)
# with open('Forwards.pickle', 'wb') as file:
#     pickle.dump(Forwards, file)
# with open('Defenders.pickle', 'wb') as file:
#     pickle.dump(Defenders, file)
#
#
#
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
# from tqdm import tqdm
# import matplotlib.pyplot as plt
#
# statsmid=Midfielders.iloc[:,9:-1]
# data_mid=StandardScaler().fit_transform(statsmid)
#
#
# PCA=PCA()
# PCA.n_components=161
# pca_data_mid = PCA.fit_transform(data_mid)
#
# percentage_var_explained = PCA.explained_variance_ / np.sum(PCA.explained_variance_);
#
# # cumulative variance explained
# cum_var_explained = np.cumsum(percentage_var_explained)
#
# plt.figure(1, figsize=(12, 6))
# plt.plot(cum_var_explained, linewidth=2)
# plt.axis('tight')
# plt.grid()
# plt.xlabel('principal components')
# plt.ylabel('Cumulative variance explained')
# plt.title('PCA: components selection')
#
#
# stats_mid=pca_data_mid[:,:101]
# from scipy.spatial import distance
#
#
#
# def getStatsmid(name):
#     index=midfielder_ID[name]
#     return stats_mid[index,:]
#
# def similiaritymid(player1,player2):
#     return 1 - distance.cosine(getStatsmid(player1), getStatsmid(player2))
#
# def normalizemid(array):
#     return np.array([round(num, 2) for num in (array - min(array))*100/(max(array)-min(array))])
#
#
#
# enginemid = {}
# for query in tqdm(mid_unique):
#     metric = []
#     for player in mid_unique:
#         value =similiaritymid(query,player)
#         metric.append(value)
#     metric = normalizemid(metric)
#     enginemid[query] = metric
#
# with open(r'pickle\enginemid.pickle', 'wb') as file:
#     pickle.dump(enginemid, file)
#
#
#
#
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
# from tqdm import tqdm
#
# statsforw=Forwards.iloc[:,9:-1]
# data_forw=StandardScaler().fit_transform(statsforw)
#
#
# PCA=PCA()
# PCA.n_components=161
# pca_data_forw = PCA.fit_transform(data_forw)
#
# percentage_var_explained = PCA.explained_variance_ / np.sum(PCA.explained_variance_);
#
# # cumulative variance explained
# cum_var_explained = np.cumsum(percentage_var_explained)
#
# plt.figure(1, figsize=(12, 6))
# plt.plot(cum_var_explained, linewidth=2)
# plt.axis('tight')
# plt.grid()
# plt.xlabel('principal components')
# plt.ylabel('Cumulative variance explained')
# plt.title('PCA: components selection')
#
#
# stats_forw=pca_data_forw[:,:101]
# from scipy.spatial import distance
#
#
#
# def getStatsforw(name):
#     index=forward_ID[name]
#     return stats_forw[index,:]
#
# def similiarityforw(player1,player2):
#     return 1 - distance.cosine(getStatsforw(player1), getStatsforw(player2))
#
# def normalizeforw(array):
#     return np.array([round(num, 2) for num in (array - min(array))*100/(max(array)-min(array))])
#
#
#
# engineforw = {}
# for query in tqdm(forw_unique):
#     metric = []
#     for player in forw_unique:
#         value =similiarityforw(query,player)
#         metric.append(value)
#     metric = normalizeforw(metric)
#     engineforw[query] = metric
#
# with open(r'pickle\engineforw.pickle', 'wb') as file:
#     pickle.dump(engineforw, file)
#
#
#
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
# from tqdm import tqdm
#
# statsdef=Defenders.iloc[:,9:-1]
# data_def=StandardScaler().fit_transform(statsdef)
#
#
# PCA=PCA()
# PCA.n_components=161
# pca_data_def = PCA.fit_transform(data_def)
#
# percentage_var_explained = PCA.explained_variance_ / np.sum(PCA.explained_variance_);
#
# # cumulative variance explained
# cum_var_explained = np.cumsum(percentage_var_explained)
#
# plt.figure(1, figsize=(12, 6))
# plt.plot(cum_var_explained, linewidth=2)
# plt.axis('tight')
# plt.grid()
# plt.xlabel('principal components')
# plt.ylabel('Cumulative variance explained')
# plt.title('PCA: components selection')
#
#
# stats_def=pca_data_def[:,:101]
# from scipy.spatial import distance
#
#
#
# def getStatsdef(name):
#     index=defender_ID[name]
#     return stats_def[index,:]
#
# def similiaritydef(player1,player2):
#     return 1 - distance.cosine(getStatsdef(player1), getStatsdef(player2))
#
# def normalizedef(array):
#     return np.array([round(num, 2) for num in (array - min(array))*100/(max(array)-min(array))])
#
#
#
# enginedef = {}
# for query in tqdm(def_unique):
#     metric = []
#     for player in def_unique:
#         value =similiaritydef(query,player)
#         metric.append(value)
#     metric = normalizedef(metric)
#     enginedef[query] = metric
#
# with open(r'pickle\enginedef.pickle', 'wb') as file:
#     pickle.dump(enginedef, file)

