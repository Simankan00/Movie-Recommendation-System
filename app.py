import pickle
import streamlit as st
import pandas as pd
import requests

# OMDb Poster Fetch Function using API key
def fetch_poster_by_title(title, year=None):
    api_key = "50983761"  # OMDb API key
    base_url = "http://www.omdbapi.com/"

    params = {
        "apikey": api_key,
        "t": title
    }
    if year:
        params["y"] = year

    try:
        response = requests.get(base_url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_url = data.get("Poster")
            if poster_url and poster_url != "N/A":
                return poster_url
    except Exception as e:
        print("Error fetching poster:", e)

    return "https://via.placeholder.com/500x750?text=No+Poster+Found"

# Recommend similar movies
def recommend(movie):
    index = movies[movies['Movie_Title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]  # Top 10

    recommended_movies = []
    recommended_movie_posters = []

    for i in movie_list:
        movie_data = movies.iloc[i[0]]
        title = movie_data.Movie_Title
        year = movie_data.get('Year', None)
        poster_url = fetch_poster_by_title(title, year)

        recommended_movies.append(title)
        recommended_movie_posters.append(poster_url)

    return recommended_movies, recommended_movie_posters

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox("Select a movie", movies['Movie_Title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    # Show posters in 2 rows of 5 columns
    for row in range(2):  # 2 rows
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            if idx < len(posters):
                with cols[i]:
                    st.image(posters[idx])
                    st.caption(names[idx])
