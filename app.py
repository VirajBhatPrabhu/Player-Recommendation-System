import streamlit as st
import pandas as pd
import pickle
from pathlib import Path


st.set_page_config(
    page_title="Player Recommendation System",
    page_icon=":soccer:"
)

@st.cache(show_spinner=False)
def getData():
    # loading outfield players' cleaned data and engine
    player_df = pd.read_pickle('Resources/outfield.pickle')
    with open('Resources/Player_ID.pickle', 'rb') as file:
        player_ID = pickle.load(file)
    with open('Resources/engine.pickle', 'rb') as file:
        engine = pickle.load(file)

    gk_df = pd.read_pickle('Resources/Goalkeeper.pickle')
    with open('Resources/Goalkeeper_ID.pickle', 'rb') as file:
        gk_ID = pickle.load(file)
    with open('Resources/engine_gk.pickle', 'rb') as file:
        gk_engine = pickle.load(file)

    return [player_df, player_ID, engine], [gk_df, gk_ID, gk_engine]

outfield_data, gk_data = getData()


header = st.container()
data_info1 = st.container()
params = st.container()
result = st.container()

with header:
    st.title('Player Recommendation System')

with data_info1:
    st.markdown('Based on the 2021/2022 season data for the Top5 European leagues')
    @st.cache
    def read_info(path):
        return Path(path).read_text(encoding='utf8')

with params:
    st.text(' \n')
    st.text(' \n')
    st.header('Play with the parameters')

    col1, col2, col3 = st.columns([1, 2.2, 0.8])
    with col1:
        radio = st.radio('Choose Player Type', ['Outfield players', 'GoalKeepers'])

    with col2:
        if radio == 'Outfield players':
            df, player_ID, engine = outfield_data
        else:
            df, player_ID, engine = gk_data
        players = sorted(list(player_ID.keys()))
        age_default = (min(df['Age']), max(df['Age']))
        query = st.selectbox('Player name', players,help='Type without deleting a character. To search from a specific team, just type in the club\'s name.')

    with col3:
        foot = st.selectbox('Preferred foot', ['All', 'Automatic', 'Right', 'Left'],
                            help='\'Automatic\' matches the preferred foot of the selected player with the players automatically. \
                            \'All\' by default. Preferred foot data is not available for GK\'s.')


    col4, col5, col6, col7 = st.columns([0.7, 1, 1, 1])
    with col4:
        if radio=='Outfield players':
            res, val, step = (5, 20), 10, 5
        else:
            res, val, step = (3, 10), 5, 1
        count = st.slider('Number of results', min_value=res[0], max_value=res[1], value=val, step=step)
    with col5:
        comp = st.selectbox('League', ['All', 'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1'],
            help='Leagues to get recommendations from. \'All\' leagues by default.')
    with col6:
        comparison = st.selectbox('Comparison with', ['All positions', 'Same position'],
            help='Whether to compare the selected player with all positions or just the same defined position in the dataset. \'All \
            positions\' by default.')
    with col7:
        age = st.slider('Age bracket', min_value=age_default[0], max_value=age_default[1], value=age_default,
        help='Age range to get recommendations from. Drag the sliders on either side. \'All\' ages by default.')

    with result:
        st.text(' \n')
        st.text(' \n')
        st.text(' \n')
        st.markdown('_These are the players most similar to_ **{}**'.format(query))


        def getRecommendations(metric, df_type, league='All', foot='All', comparison='All positions', age=age_default,
                               count=val):
            if df_type == 'outfield':
                df_res = df.iloc[:, [1, 3, 5, 6, 10, -1]].copy()
            else:
                df_res = df.iloc[:, [1, 3, 5, 6, 10]].copy()
            df_res['Player'] = list(player_ID.keys())
            df_res.insert(1, 'Similarity', metric)
            df_res = df_res.sort_values(by=['Similarity'], ascending=False)
            metric = [str(num) + '%' for num in df_res['Similarity']]
            df_res['Similarity'] = metric
            df_res = df_res.iloc[1:, :]

            if comparison == 'Same position' and df_type == 'outfield':
                q_pos = list(df[df['Player'] == query.split(' (')[0]].Pos)[0]
                df_res = df_res[df_res['Pos'] == q_pos]

            if league == 'All':
                pass
            else:
                df_res = df_res[df_res['Comp'] == league]

            if age == age_default:
                pass
            else:
                df_res = df_res[(df_res['Age'] >= age[0]) & (df_res['Age'] <= age[1])]

            if foot == 'All' or df_type == 'gk':
                pass
            elif foot == 'Automatic':
                query_foot = df['Foot'][player_ID[query]]
                df_res = df_res[df_res['Foot'] == query_foot]
            elif foot == 'Left':
                df_res = df_res[df_res['Foot'] == 'left']
            else:
                df_res = df_res[df_res['Foot'] == 'right']

            df_res = df_res.iloc[:count, :].reset_index(drop=True)
            df_res.index = df_res.index + 1
            if len(df) == 2077:
                mpmin = [str(num) for num in df_res['Min']]
                df_res['Min'] = mpmin
            df_res.rename(columns={'Pos': 'Position', 'Comp': 'League','Min':'Mins played'}, inplace=True)
            return df_res


        sims = engine[query]
        df_type = 'outfield' if len(df) == 2077 else 'gk'
        recoms = getRecommendations(sims, df_type=df_type, foot=foot, league=comp, comparison=comparison, age=age,
                                    count=count)
        st.table(recoms)



