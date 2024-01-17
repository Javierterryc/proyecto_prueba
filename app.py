import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import os

# st.markdown('---')
left,right = st.columns([3,1])
with left:
    st.title('Youtube & Spotify analysis')
    st.subheader('Data visualization',divider='grey')
with right:
    st.image('YTSPT.png', width=150)

st.write('In the following interactive dashboard we will present our solution focused on the analysis and visualisation of features of songs played on the streaming platforms Spotify and Youtube. We have used a database available on the Kaggle platform, which hosts detailed information on 20,717 songs collected on 23 February 2023, covering a total of 25 variables per song.')
st.write("We chose this [dataset](https://www.kaggle.com/datasets/salvatorerastelli/spotify-and-youtube/data) from *Kaggle*.")


# TOP artists on spotify(streams) and youtube(views)
    
st.markdown('---')
df_views = pd.read_csv(r'df_views.csv',encoding = 'ISO-8859-1',delimiter=',')
df_streams = pd.read_csv(r'df_streams.csv',encoding = 'ISO-8859-1',delimiter=',')
selected_metric = st.selectbox("Please choose a metric:", ['Youtube','Spotify'])

if selected_metric=='Youtube':
    st.header("Top 10 artists on :red[Youtube]", divider='red')
    fig = go.Figure(px.bar(df_views, x='Artist', y='Views',
                width=700,height=500
                ))
    fig.update_traces(marker = dict(color='#FF0000'))
    st.plotly_chart(fig)
    selected_artist = st.selectbox("Please choose a singer:",
                                    ['CoComelon','Katy Perry','Charlie Puth','Ed Sheeran','Luis Fonsi',
                                     'Justin Bieber','Daddy Yankee','Bruno Mars','Coldplay'])
    output_folder = 'yt_artists'
    file_to_read = f'{selected_artist.replace(" ", "_")}.csv'
    file_path = os.path.join(output_folder, file_to_read)
    df_read = pd.read_csv(file_path)
    fig = go.Figure(px.bar(df_read, x='Views', y='Track',
                          orientation='h',
                          width=700,height=500))
    
    fig.update_traces(marker = dict(color='#FF0000'),width=0.5)
    # fig.update_traces(marker = colour[metric], )
    st.plotly_chart(fig)

else:
    st.header("Top 10 artists on :green[Spotify]", divider='green')
    fig = go.Figure(px.bar(df_streams, x='Artist', y='Stream',
                width=700,height=500
                ))
    fig.update_traces(marker = dict(color='#1ED760')) # Spotify color: #1ED760
    # marker = dict(color='#87faed')
    st.plotly_chart(fig)
    selected_artist = st.selectbox("Please choose a singer:",
                                    ['Post Malone','Ed Sheeran','Dua Lipa','XXXTENTACION','The Weeknd',
                                    'Justin Bieber','Imagine Dragons','Coldplay','Khalid','Bruno Mars'])
    output_folder = 'sp_artists'
    file_to_read = f'{selected_artist.replace(" ", "_")}.csv'
    file_path = os.path.join(output_folder, file_to_read)
    df_read = pd.read_csv(file_path)
    fig = go.Figure(px.bar(df_read, x='Stream', y='Track',
                          orientation='h',
                          width=700,height=500))
    
    fig.update_traces(marker = dict(color='#1ED760'),width=0.5)
    st.plotly_chart(fig)


st.header("Best :blue[**artists**]", divider='blue')
left,right = st.columns([1,2.85])
with left:
  colour = {'Views':{'color':'blue'}, 'Likes': {'color':'grey'},
            'Comments': {'color':'purple'}}
  metric = st.radio("Show me the best artists in terms of their:",
                    ["Views", "Likes", "Comments"],)

with right:
  df_views = pd.read_csv(r'df_likes.csv',encoding = 'ISO-8859-1',delimiter=',')
  fig = go.Figure(px.bar(df_views,x="Artist",
                                  y=metric,
                                  #title=metric,
                                  width=490,height=500))
  codes = {'Views':'#f37736', 'Likes': '#7bc043',
          'Comments': '#0392cf'}
  fig.update_layout(title=f'Best artist depending on {metric}',
                    title_x=0.3,title_y=0.95,)
  # Colores a usar: #87cefa,	#fa87ce,	#cefa87
  fig.update_traces(marker = dict(color=codes[metric]), 
                    width=0.5)
  st.plotly_chart(fig)



# Metrics
st.header("Interesting metrics",divider='rainbow')
df_metrics = pd.read_csv(r'df_metrics.csv',encoding = 'ISO-8859-1',delimiter=',')

metric = st.selectbox("Please choose a metric:", ['Danceability', 'Energy', 'Valence'])
codes = {'Danceability': '#00c2c7', 'Energy': '#f9d62e',
          'Valence': '#ef4f91'}
description = {'Danceability':'**Danceability**: describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.',
           'Energy':'**Energy**: is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale.',
           'Valence':'**Valence**: a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive, while tracks with low valence sound more negative'}
fig = go.Figure(px.bar(df_metrics,x="Artist",
                                y=metric,
                                width=750,height=500))
fig.update_traces(marker = dict(color=codes[metric]))
fig.update_yaxes(range = [0,1]) # We set the y-axis from 0 to 1
st.write(description[metric])
st.plotly_chart(fig)

st.header("How are metrics correlated?",divider='grey')

option1 = st.selectbox('Choose x-axis:',['Likes', 'Comments','Views'])
if option1 == 'likes':
   list = ['Comments','Views']
elif option1 == 'Comments':
   list = ['Likes','Views']
else:
   list = ['Comments','Likes']
   
option2 = st.selectbox('Choose y-axis:',list)

# options = st.multiselect(
#     'Select two variables',
#     ['Likes', 'Comments','Views'],
#     placeholder='Select',
#     default = ['Likes', 'Comments'],
#     max_selections = 2)

metric_1 = option1
metric_2 = option2

df = pd.read_csv(r'Spotify_Youtube.csv',encoding = 'ISO-8859-1',delimiter=',')
fig = go.Figure(px.scatter(df, x=metric_1, y=metric_2, 
                          title=f"{metric_1} vs {metric_2}",
                          color="Artist", hover_name='Track', 
                          hover_data=['Title', 'Artist'], opacity=0.7))

fig.update_layout(xaxis_title=metric_1, yaxis_title=metric_2, 
                  xaxis_type='log', yaxis_type='log')
fig.update_traces(marker=dict(size=7))
st.plotly_chart(fig)


#       [theme]
#       backgroundColor="#7b1818"
#       secondaryBackgroundColor="#a1fb9e"
#       textColor="#f4f5f9"

#       Diccionario de colores: https://www.color-hex.com/color/87cefa
#       cd C:\Users\javie\Desktop\Proyecto_visualizacion 
#       venv\Scripts\activate 
#       streamlit run .\prueba2.py 

