import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
from st_aggrid import GridOptionsBuilder, AgGrid
st.set_page_config(
    page_title="Player Recommendation System",
    page_icon=":soccer:"
)
st.markdown("<h1 style='text-align: center; color: #ff4d4d;'>Player Recommendation System</h1>", unsafe_allow_html=True)


def table(data):
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
    gb.configure_side_bar()  # Add a sidebar
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        theme='dark',  # Add theme color to the table
        enable_enterprise_modules=False,
        height=350,
        reload_data=False
    )

@st.cache(show_spinner=False)
def getData():
    midfielders_df = pickle.load(open('Midfielders.pkl', 'rb'))
    with open('Resources/midfielder_ID.pickle', 'rb') as file:
        midfielder_ID = pickle.load(file)
    with open('Resources/enginemid.pickle', 'rb') as file:
        enginemid = pickle.load(file)

    defenders_df = pickle.load(open('Defenders.pkl', 'rb'))
    with open('Resources/defender_ID.pickle', 'rb') as file:
        defender_ID = pickle.load(file)
    with open('Resources/enginedef.pickle', 'rb') as file:
        enginedef = pickle.load(file)

    forwards_df = pickle.load(open('Forwards.pkl', 'rb'))
    with open('Resources/forward_ID.pickle', 'rb') as file:
        forward_ID = pickle.load(file)
    with open('Resources/engineforw.pickle', 'rb') as file:
        engineforw = pickle.load(file)

    gk_df = pickle.load(open('GK.pickle', 'rb'))
    with open('Resources/Goalkeeper_ID.pickle', 'rb') as file:
        gk_ID = pickle.load(file)
    with open('Resources/engine_gk.pickle', 'rb') as file:
        gk_engine = pickle.load(file)

    return [midfielders_df, midfielder_ID, enginemid], [defenders_df, defender_ID, enginedef], [forwards_df, forward_ID,
                                                                                                engineforw], [gk_df,
                                                                                                              gk_ID,
                                                                                                              gk_engine]


midfielder_data, defender_data, forward_data, gk_data = getData()

params = st.container()
result = st.container()



with params:
    st.text(' \n')
    st.text(' \n')
    st.text('Data is based on 21/22 Season for the Big 5 European Leagues')
    st.text(' \n')
    st.text(' \n')

    col1, col2, col3 = st.columns([1.2,1,2.8])
    with col1:
        radio = st.radio('Choose a Position', ['Defenders', 'Midfielders', 'Forwards', 'GoalKeepers'])

    with col2:
        foot = st.selectbox('Preferred foot', ['All', 'Automatic', 'Right', 'Left'])


    with col3:
        if radio == 'Midfielders':
            df, player_ID, engine = midfielder_data

        elif radio == 'Defenders':
            df, player_ID, engine = defender_data

        elif radio == 'Forwards':
            df, player_ID, engine = forward_data

        else:
            df, player_ID, engine = gk_data

        players = sorted(list(player_ID.keys()))
        age_default = (min(df['Age']), max(df['Age']))
        query = st.selectbox('Player', players)

    st.text(' \n')
    st.text(' \n')


    col4, col5, col6, col7 = st.columns([1, 1, 1, 1])

    with col4:
        comp = st.selectbox('League', ['All', 'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1'],)


    with col5:
        if radio == 'Midfielders':
            res, val, step = (10, 20), 10, 5

        elif radio == 'Defenders':
            res, val, step = (10, 20), 10, 5

        elif radio == 'Forwards':
            res, val, step = (10, 20), 10, 5


        else:
            res, val, step = (10, 20), 10, 5
        count = st.slider('Number of Players', min_value=res[0], max_value=res[1], value=val, step=step)


    with col6:
        age = st.slider('Age Bracket', min_value=age_default[0], max_value=age_default[1], value=age_default)

    with col7:
        comparison = st.selectbox('Compare with', ['All positions', 'Same position'])

    with result:
        st.text(' \n')
        st.text(' \n')



        def getRecommendations(metric, df_type, league='All', foot='All', comparison='All positions', age=age_default,count=val):

            if df_type == 'Midfield':
                df_res = df.iloc[:, [0,1,4,5,-1]].copy()

            elif df_type == 'Defense':
                df_res = df.iloc[:, [0,1,4,5,-1]].copy()

            elif df_type == 'Forward':
                df_res = df.iloc[:, [0,1,4,5,-1]].copy()
            else:
                df_res = df.iloc[:, [0,1,3,4,5]].copy()
            df_res['Player'] = list(player_ID.keys())
            df_res.insert(1, 'Similarity', metric)
            df_res = df_res.sort_values(by=['Similarity'], ascending=False)
            metric = [str(num) + '%' for num in df_res['Similarity']]
            df_res['Similarity'] = metric
            df_res = df_res.iloc[1:, :]

            if comparison == 'Same position' and df_type == 'Midfield':
                q_pos = list(df[df['Player'] == query.split(' (')[0]].Pos)[0]
                df_res = df_res[df_res['Pos'] == q_pos]

            elif comparison == 'Same position' and df_type == 'Defense':
                q_pos = list(df[df['Player'] == query.split(' (')[0]].Pos)[0]
                df_res = df_res[df_res['Pos'] == q_pos]

            elif comparison == 'Same position' and df_type == 'Forward':
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
            df_res.rename(columns={'Pos': 'Position', 'Comp': 'League'}, inplace=True)
            return df_res


        sims = engine[query]
        if len(df) == 609:
            df_type = 'Midfield'
        elif len(df) == 772:
            df_type= 'Defense'
        elif len(df) == 460:
            df_type= 'Forward'
        else:
            df_type= 'gk'

        if st.button('Recommend'):
            st.text(' \n')
            st.text(' \n')
            st.text(' \n')
            st.markdown('Recommending players similar to **{}**'.format(query))

            recoms = getRecommendations(sims, df_type=df_type, foot=foot, league=comp, comparison=comparison, age=age,count=count)
            table(recoms)
