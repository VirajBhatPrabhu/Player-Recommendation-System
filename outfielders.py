import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from tqdm import tqdm
import pickle

redundant = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s']

Standard = pd.read_excel('Outfielders/Standard.xlsx').drop(['Rk'], axis=1)
Defense = pd.read_excel('Outfielders/Defense.xlsx').drop(redundant, axis=1)
Gca = pd.read_excel('Outfielders/Goal-shotcreation.xlsx').drop(redundant, axis=1)
Passtypes = pd.read_excel('Outfielders/Passtype.xlsx').drop(redundant, axis=1)
Possession = pd.read_excel('Outfielders/Posession.xlsx').drop(redundant, axis=1)
Shooting = pd.read_excel('Outfielders/Shoot.xlsx').drop(redundant, axis=1)
Misc = pd.read_excel('Outfielders/miscallaneous.xlsx').drop(redundant, axis=1)
Passing = pd.read_excel('Outfielders/passing.xlsx').drop(redundant, axis=1)


def renamecols(table_no, dataframe):
    num = str(table_no) + "_"
    return dataframe.rename(columns=lambda x: num + x)


Defense = renamecols(2, Defense)
Gca = renamecols(3, Gca)
Passtypes = renamecols(8, Passtypes)
Possession = renamecols(5, Possession)
Shooting = renamecols(6, Shooting)
Misc = renamecols(7, Misc)
Passing = renamecols(4, Passing)

final_table = pd.concat([Standard, Defense, Gca, Passtypes, Possession, Shooting, Misc, Passing], axis=1)

df = final_table[final_table['90s'] >= 3]
df = df[df['Pos'] != 'GK'].reset_index()

df['Comp'] = df['Comp'].str.split(' ', expand=True, n=1)[1]
df['Nation'] = df['Nation'].str.split(' ', expand=True, n=1)[1]
df = df.fillna(0)
df['Age'] = df['Age'].astype(int)
df['Player'].duplicated().sum()

players = []

for i in range(len(df)):
    players.append(df['Player'][i] + ' ({})'.format(df['Squad'][i]))

Player_ID = dict(zip(players, np.arange(len(players))))

with open('Player_ID.pickle', 'wb') as file:
    pickle.dump(Player_ID, file)

Footed = []

for i in range(len(df)):

    val = df['8_Left'][i] / (df['8_Right'][i])
    if val > 1:
        Footed.append('left')
    else:
        Footed.append('right')

df['Foot'] = Footed

with open('outfield.pickle', 'wb') as file:
    pickle.dump(df, file)

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

stats = df.iloc[:, 12:-1]
data = StandardScaler().fit_transform(stats)

PCA = PCA()
PCA.n_components = 161
pca_data = PCA.fit_transform(data)

percentage_var_explained = PCA.explained_variance_ / np.sum(PCA.explained_variance_)

# cumulative variance explained
cum_var_explained = np.cumsum(percentage_var_explained)
#
# plt.figure(1, figsize=(12, 6))
# plt.plot(cum_var_explained, linewidth=2)
# plt.axis('tight')
# plt.grid()
# plt.xlabel('principal components')
# plt.ylabel('Cumulative variance explained')
# plt.title('PCA: components selection')

stats = pca_data[:, :99]

from scipy.spatial import distance


def getstats(name):
    index = Player_ID[name]
    return stats[index, :]


def similiarity(player1, player2):
    return 1 - distance.cosine(getstats(player1), getstats(player2))


def normalize(array):
    return np.array([round(num, 2) for num in (array - min(array)) * 100 / (max(array) - min(array))])


engine = {}
for query in tqdm(players):
    metric = []
    for player in players:
        value = similiarity(query, player)
        metric.append(value)
    metric = normalize(metric)
    engine[query] = metric

with open('engine.pickle', 'wb') as file:
    pickle.dump(engine, file)
