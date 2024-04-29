import streamlit as st
import pandas as pd

st.set_page_config(layout='wide', page_title='Players Analysis')

data = pd.read_csv('/Users/ankitkhatkar/PycharmProjects/StreamLit/Resources/ipl_deliveries.csv')

def player_details(player):

    cl1, cl2, cl3, cl4 = st.columns(4)

    played_matches = data[(data['batter'] == player) | (data['bowler'] == player)]
    total = played_matches['ID'].nunique()

    with cl1:
        st.metric('Matches Played',str(total))

    as_batsman = data[data['batter']==player]
    total_runs = as_batsman['batsman_run'].sum()

    with cl2:
        st.metric('Total runs as a batsman', str(total_runs))

    max_runs_as_batsman = str(as_batsman.groupby('ID')['batsman_run'].sum().sort_values(ascending=False).iloc[0])

    with cl3:
        st.metric('Highest score as a batsman', str(max_runs_as_batsman))

    batter = as_batsman.groupby('ID', as_index=False)['batsman_run'].sum()
    half_centuries = batter[(batter['batsman_run'] >= 50) & (batter['batsman_run'] < 100)].shape[0]
    centuries = batter[batter['batsman_run'] >= 100].shape[0]
    fifty_hundred = f'{half_centuries}/{centuries}'

    with cl4:
        st.metric('50s/100s', fifty_hundred)

st.sidebar.title('Player Analysis')
selected = st.sidebar.selectbox('Select one', ['Overall Analysis', 'Player'])
if selected == 'Overall Analysis':
    st.title('Overall Analysis')
    st.dataframe(data.describe())
else:
    player = st.sidebar.selectbox('Select Player',(sorted(data['batter'].sort_values(ascending=False).unique().tolist())))
    btn1 = st.sidebar.button('Show Player Details')
    if btn1:
        st.title(player)
        player_details(player)
