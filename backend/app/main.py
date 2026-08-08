from fastapi import FastAPI
import pickle

app = FastAPI()

movies = pickle.load(open("app/movies.pkl", "rb"))
similarity = pickle.load(open("app/similarity.pkl", "rb"))


@app.get("/")
def home():
    return {"message": "CineMind API is running!"}

@app.get("/recommend/{movie_name}")
def recommend(movie_name: str):

    movie_name = movie_name.lower()

    matches = movies[movies['title'].str.lower() == movie_name]

    if matches.empty:
        return {
            "message": "Movie not found",
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
        recommendations.append(movies.iloc[i[0]]['title'])

    return {
        "movie": movies.iloc[movie_index]['title'],
        "recommendations": recommendations
    }