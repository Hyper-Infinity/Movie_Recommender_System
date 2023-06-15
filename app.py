import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle

movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
df = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(num):
    url = f"https://api.themoviedb.org/3/movie/{num}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwZTMzZTY2ODdmOWFhMDkyYzBjOTZkYmYxZTNiNzRlMCIsInN1YiI6IjY0ODBiOTE1YmYzMWYyMDEzYWRjN2EwNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0_97MwRZYYMqMqR1EUHv899exylrbcbu9mixgHVMTIg"
    }

    response = requests.get(url, headers=headers)

    return "https://image.tmdb.org/t/p/original" + response.json()['poster_path']


def recommendation_task(movie):

    movie_index = df[df['title'] == movie].index[0]
    dist = similarity[movie_index]
    recommend_movie_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1: 6]

    movie_name = list()
    movie_id = list()
    for i in recommend_movie_list:
        movie_name.append(df.loc[i[0], 'title'])
        movie_id.append(df.loc[i[0], 'movie_id'])
    return movie_name, movie_id


st.set_page_config(layout="wide")

st.title('WELCOME TO MOVIE RECOMMENDATION SYSTEM')

st.write('<p style="font-size:21px; color:#6af0f7;"> I Will Recommend You More Of Your Interest </p>', unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Enter Movie Here",
    df['title'].values)

if st.button('Recommend'):
    Name, Id = recommendation_task(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(Name[0])
        st.image(fetch_poster(Id[0]))

    with col2:
        st.write(Name[1])
        st.image(fetch_poster(Id[1]))

    with col3:
        st.write(Name[2])
        st.image(fetch_poster(Id[2]))

    with col4:
        st.write(Name[3])
        st.image(fetch_poster(Id[3]))

    with col5:
        st.write(Name[4])
        st.image(fetch_poster(Id[4]))

