from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import json

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

app = FastAPI()

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML data
movies = pickle.load(open("app/movies.pkl", "rb"))
similarity = pickle.load(open("app/similarity.pkl", "rb"))
movie_metadata = pd.read_csv("../dataset/tmdb_5000_movies.csv")

@app.get("/")
def home():
    return {"message": "CineMind API is running!"}


@app.get("/search/{query}")
def search_movies(query: str):

    query = query.lower().strip()

    if not query:
        return {"movies": []}

    matches = movies[
        movies["title"].str.lower().str.contains(query, na=False)
    ]

    results = matches["title"].head(10).tolist()

    return {
        "movies": results
    }
def get_movie_details(title):

    if not TMDB_API_KEY:
        return {
            "poster": None,
            "tmdb_rating": None
        }

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": title
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("results"):
            movie = data["results"][0]

            poster_path = movie.get("poster_path")

            poster_url = None

            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

            return {
                "poster": poster_url,
                "tmdb_rating": movie.get("vote_average")
            }

    except Exception:
        pass

    return {
        "poster": None,
        "tmdb_rating": None
    }
@app.get("/recommend/{movie_name}")
def recommend(movie_name: str):

    movie_name = movie_name.lower().strip()

    matches = movies[
        movies["title"].str.lower() == movie_name
    ]

    if matches.empty:
        return {
            "movie": movie_name,
            "recommendations": []
        }

    movie_index = matches.index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movies_list:

        title = movies.iloc[i[0]]["title"]

        metadata_match = movie_metadata[
            movie_metadata["title"].str.lower() == title.lower()
        ]

        if not metadata_match.empty:

            metadata = metadata_match.iloc[0]

            overview = metadata["overview"]

            if pd.isna(overview):
                overview = "No overview available."

            release_date = metadata["release_date"]

            if pd.isna(release_date):
                release_year = "N/A"
            else:
                release_year = str(release_date)[:4]

            rating = metadata["vote_average"]

            if pd.isna(rating):
                rating = 0

            movie_details=get_movie_details(title)
            recommendations.append({
                "title": title,
                "overview": overview,
                "release_year": release_year,
                "rating": float(rating),
                "poster":movie_details["poster"]
            })

        else:

            recommendations.append({
                "title": title,
                "overview": "No overview available.",
                "release_year": "N/A",
                "rating": 0
            })

    return {
        "movie": movies.iloc[movie_index]["title"],
        "recommendations": recommendations
    }