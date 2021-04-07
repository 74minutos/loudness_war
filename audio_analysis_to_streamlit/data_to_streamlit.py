import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_icon="assets\favicon.ico",
                   layout='wide')
st.title('Loudness Analysis')
url_data = "https://github.com/74minutos/loudness_war/blob/main/results/joined_data.csv?raw=true"
data = pd.read_csv(url_data, sep=";")

st.markdown("This is a little personal geek project where you can find a loudness analysis for over 6.000 songs")

song = st.sidebar.multiselect(
    'Which song do you want to analyze?',
     (data.track_name + " - " + data.artist_name).unique())

for i in song:
    'You selected: ', i
    mask = data.track_name + " - " + data.artist_name == i
    filtered_data = data.loc[mask, :]

    chart = alt.Chart(filtered_data).mark_line().encode(
        alt.X('time'),
        alt.Y('loudness',
            scale=alt.Scale(domain=(-60, 5))
        ))
    st.altair_chart(chart, use_container_width=True)
