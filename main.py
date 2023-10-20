import pickle
import streamlit as st
import requests
import pandas as pd
print('working')

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    #print(data)
    try:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        full_path="https://img.freepik.com/free-vector/flat-design-no-photo-sign-design_23-2149288658.jpg?w=740&t=st=1697303670~exp=1697304270~hmac=69dafd32846e1090dddc7fbf9c46eee1aa05aedd1a5371a959daadd263d93c6c"
    #print(full_path)
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[0:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].imdbId
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommendation System')
movies1 = pickle.load(open('new1.pkl','rb'))
movies=pd.DataFrame(movies1)
similarity = pickle.load(open('simi.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
if st.button('Show Recommendation'):
    recommended_movie_names,ab = recommend(selected_movie)
    columns = st.columns(6)
    for i in range(6):
        with columns[i]:
            st.write(recommended_movie_names[i], unsafe_allow_html=True)
            st.image(ab[i])
