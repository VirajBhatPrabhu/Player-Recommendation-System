import pandas as pd
import numpy as np
import scipy
from tqdm import tqdm
import pickle

redundant = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s']

Goalkeeping = pd.read_excel('Goalkeepers/Goalkeeping.xlsx').drop(['Rk'], axis=1)
AdvancedGk = pd.read_excel('Goalkeepers/AdvanceGoalkeeping.xlsx').drop(redundant, axis=1)


def renamecols(table_no, df):
    num = str(table_no) + "_"
    return df.rename(columns=lambda x: num + x)


AdvancedGk = renamecols(2, AdvancedGk)

grand = pd.concat([Goalkeeping, AdvancedGk], axis=1)
GK = grand[grand['Pos'] == 'GK']

df = GK[GK['90s'] >= 3].reset_index()

df['Comp'] = df['Comp'].str.split(' ', expand=True, n=1)[1]
df['Nation'] = df['Nation'].str.split(' ', expand=True, n=1)[1]

df = df.fillna(0)

with open('Goalkeeper.pickle', 'wb') as file:
    pickle.dump(df, file)

Gks = []

for i in range(len(df)):
    Gks.append(df['Player'][i] + ' ({})'.format(df['Squad'][i]))

Goalkeeper_ID = dict(zip(Gks, np.arange(len(Gks))))

with open('Goalkeeper_ID.pickle', 'wb') as file:
    pickle.dump(Goalkeeper_ID, file)

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

stats = df.iloc[:, 12:-1]
data = StandardScaler().fit_transform(stats)

PCA = PCA()
PCA.n_components = 39
pca_data = PCA.fit_transform(data)

per_var = PCA.explained_variance_ / np.sum(PCA.explained_variance_)
cum_variance = np.cumsum(per_var)

# plt.figure(1, figsize=(12, 6))
# plt.plot(cum_variance, linewidth=2)
# plt.axis('tight')
# plt.grid()
# plt.xlabel('principal components')
# plt.ylabel('Cumulative variance explained')
# plt.title('PCA: components selection')
#


from scipy.spatial import distance

stats = pca_data[:, :25]


def getstats(name):
    index = Goalkeeper_ID[name]
    return stats[index, :]


def similiarity(player1, player2):
    return 1 - distance.cosine(getstats(player1), getstats(player2))


def normalize(array):
    return np.array([round(num, 2) for num in (array - min(array)) * 100 / (max(array) - min(array))])


engine_gk = {}
for query in tqdm(Gks):
    metric = []
    for player in Gks:
        value = similiarity(query, player)
        metric.append(value)
    metric = normalize(metric)
    engine_gk[query] = metric

with open('engine_gk.pickle', 'wb') as file:
    pickle.dump(engine_gk, file)
