# 🎬 CineMind — AI Movie Recommendation System

CineMind is an AI-powered movie recommendation system that recommends movies based on the user's selected movie.

The project combines a **Machine Learning content-based recommendation system**, **FastAPI backend**, **React frontend**, and **TMDB API** to provide an interactive movie discovery experience.


## ✨ Features

- 🎬 Content-based movie recommendation
- 🔍 Movie search and autocomplete
- ⭐ Movie ratings and release years
- 🖼️ Dynamic movie posters using TMDB API
- 🤖 Machine Learning based similarity matching
- ⚡ FastAPI REST API
- ⚛️ React-based frontend
- ⏳ Loading and error states
- 📱 Responsive cinematic UI
- 🖤 Red & black movie-platform inspired theme

## 🧠 How It Works

CineMind uses a **content-based filtering approach**.

Movie information such as genres, keywords, cast, crew and other relevant metadata is combined into a textual representation.

The text is then converted into numerical vectors using **TF-IDF vectorization**.

Cosine similarity is used to calculate how similar movies are to one another.

### Recommendation Pipeline

```text
Movie Dataset
      ↓
Data Cleaning & Preprocessing
      ↓
Feature Engineering
      ↓
Text Combination
      ↓
TF-IDF Vectorization
      ↓
Cosine Similarity
      ↓
Top Similar Movies
      ↓
FastAPI Backend
      ↓
React Frontend
      ↓
Movie Recommendations

## 🛠️ Tech Stack
Machine Learning
Python
Pandas
NumPy
Scikit-learn
TF-IDF Vectorization
Cosine Similarity

Backend
FastAPI
Python
REST API
Uvicorn

External API
TMDB API for movie posters and metadata

Development Tools
Jupyter Notebook
VS Code
Git
GitHub



Feel free to explore the repository and give it a ⭐ on GitHub.
