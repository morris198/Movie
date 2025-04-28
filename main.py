from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from typing import List
from starlette.responses import FileResponse
from urllib.parse import quote
import requests  # Add this line to import the 'requests' module


app = FastAPI(debug=True)


class Movie(BaseModel):
    title: str

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/549?api_key=7d110d80ffcba3c1ffc2658585e440a6&language=en-US".format(movie_id)
    data = requests.get(url, timeout=60)
    
    
    if data.status_code != 200:
        raise HTTPException(status_code=data.status_code, detail="Error fetching movie data")
    
    try:
        data = data.json()
        
        if 'poster_path' in data:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            raise HTTPException(status_code=404, detail="Poster path not found in the movie data")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing movie data: {}".format(str(e)))


def recommend(movie_title, movies, similarity):
    index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies.append({
                "title": movies.iloc[i[0]].title,
                "poster_url": poster_url
            })

    return recommended_movies

movies = joblib.load(open('movie_list.pkl', 'rb'))
similarity = joblib.load(open('similarity.pkl', 'rb'))

@app.post("/recommend")
def get_recommendations(movie: Movie):
    recommended_movies = recommend(movie.title, movies, similarity)
    return recommended_movies

@app.get("/poster/{movie_id}")
def get_movie_poster(movie_id: int):
    poster_url = fetch_poster(movie_id)
    return FileResponse(poster_url)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
