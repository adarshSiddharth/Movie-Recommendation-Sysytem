import streamlit as st
import pickle
import pandas as pd
import requests


api_key = "f55c7ce16b8c6638937063ad42811299"


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    try:
       
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f55c7ce16b8c6638937063ad42811299&language=en-US"
        response = requests.get(url, timeout=10) 
        response.raise_for_status()  
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Connection+Error"
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=API+Error"
    except Exception as e:
        print(f"Unexpected error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters


st.title('🎬 Movie Recommendation System')

option = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Show Recommendation'):
    names, posters = recommend(option)

  
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
