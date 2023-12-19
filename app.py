import joblib
import streamlit as st
import requests

st.set_page_config(
    page_title="Movie Time",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=7d110d80ffcba3c1ffc2658585e440a6&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = joblib.load(open('movie_list.pkl','rb'))
similarity = joblib.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    def format_movie_names(movie_name):
        words = movie_name.split()
        if len(words) > 2:
            return "<br>".join([" ".join(words[:len(words)//2]), " ".join(words[len(words)//2:])])
        else:
            return movie_name

    with col1:
        st.image(recommended_movie_posters[0])
        st.markdown(format_movie_names(recommended_movie_names[0]), unsafe_allow_html=True)

    with col2:
        st.image(recommended_movie_posters[1])
        st.markdown(format_movie_names(recommended_movie_names[1]), unsafe_allow_html=True)

    with col3:
        st.image(recommended_movie_posters[2])
        st.markdown(format_movie_names(recommended_movie_names[2]), unsafe_allow_html=True)

    with col4:
        st.image(recommended_movie_posters[3])
        st.markdown(format_movie_names(recommended_movie_names[3]), unsafe_allow_html=True)

    with col5:
        st.image(recommended_movie_posters[4])
        st.markdown(format_movie_names(recommended_movie_names[4]), unsafe_allow_html=True)