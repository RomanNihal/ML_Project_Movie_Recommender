import streamlit as st
import pandas as pd
import pickle
import requests

st.title('Movie Recommender System')
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('movies_similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=dcf559a2f510165fe6383caa99cc7971&language=en-US")
    response = response.json()
    return "https://image.tmdb.org/t/p/original" + response['poster_path']


def recommend(movie):
    similarity_index = movies[movies['title'] == movie].index[0]
    recommended_list = sorted(list(enumerate(similarity[similarity_index])), reverse=True, key=lambda x: x[1])[1:6]

    top_5 = []
    top_5_posters = []
    for i in recommended_list:
        top_5.append(movies.iloc[i[0]].title)
        top_5_posters.append(fetch_poster(movies.iloc[i[0]].id))
    return top_5, top_5_posters

selected_movie = st.selectbox('Select Your Favourite Movie',movies['title'].values)

if st.button('Recommend'):

    top_5_recommended_movies, top_5_recommended_movies_posters = recommend(selected_movie)

    cols = st.columns(5)  # Create 5 equal-width columns for the 5 movies
    for i in range(5):
        with cols[i]:  # Place each movie in its own column
            st.image(top_5_recommended_movies_posters[i], use_container_width=True)  # Display the poster
            st.write(f"**{top_5_recommended_movies[i]}**")  # Display the title below th