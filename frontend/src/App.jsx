import { useState,useEffect } from "react";
import "./App.css";

function App() {
  const [movie, setMovie] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [suggestions, setSuggestions] = useState([]);
 
  const searchMovies = async (query) => {
  if (!query.trim()) {
    setSuggestions([]);
    return;
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/search/${encodeURIComponent(query)}`
    );

    console.log("Search response:", response.status);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json();

    console.log("Search data:", data);

    setSuggestions(data.movies);
  } catch (error) {
    console.error("SEARCH ERROR:", error);
    setSuggestions([]);
  }
};
  const getRecommendations = async () => {
    
    if (!movie.trim()) {
      setError("Please enter a movie name.");
      return;
    }

    setLoading(true);
    setError("");
    setRecommendations([]);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/recommend/${encodeURIComponent(movie)}`
      );

      const data = await response.json();

      if (data.recommendations.length === 0) {
        setError("Movie not found. Try another movie.");
      } else {
        setRecommendations(data.recommendations);
      }
    } catch (error) {
  console.error(error);
  setError("Unable to connect to CineMind backend.");
  setRecommendations([]);
  setLoading(false);
}
finally {
  setLoading(false);
}

    setLoading(false);
  };
{!loading && !error && movie && recommendations.length === 0 && (
  <div className="empty-state">
    <div className="empty-icon">🎬</div>
    <h3>No recommendations found</h3>
    <p>
      We couldn't find this movie. Try searching for another movie.
    </p>
  </div>
)}
  return (
    <div className="app">
      <nav className="navbar">
        <div className="logo">🎬 CineMind</div>
        <div className="nav-description">
    AI-Powered Movie Recommendation System
  </div>
      </nav>

      <main className="hero-title">
        <h2>Find Your Next
        <span>Favorite Movie 🎥</span></h2>

        <p className="subtitle">
          Enter a movie you love and let CineMind recommend movies you'll enjoy.
        </p>

        <div className="search-box">
          <input
            type="text"
            placeholder="Enter a movie name..."
            value={movie}
            onChange={(e) => {
  setMovie(e.target.value);
  searchMovies(e.target.value);
}}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                getRecommendations();
              }
            }}
          />

          {suggestions.length > 0 && (
  <div className="suggestions">
    {suggestions.map((suggestion, index) => (
      <div
        key={index}
        className="suggestion"
        onClick={() => {
          setMovie(suggestion);
          setSuggestions([]);
        }}
      >
        🎬 {suggestion}
      </div>
    ))}
  </div>
)}

          <button onClick={getRecommendations}>
            {loading ? "Finding..." : "Recommend"}
          </button>
        </div>

        {error && <p className="error">{error}</p>}

        {recommendations.length > 0 && (
          <section className="results">
  <div className="results-header">
    <h2>Because you liked "{movie}"</h2>
    <p>Here are 5 movies CineMind thinks you'll enjoy.</p>
  </div>

  <div className="movie-grid">
    {recommendations.map((movie, index) => (
      <div className="movie-card" key={index}>

  <div className="movie-number">
    {index + 1}
  </div>

  {movie.poster ? (
    <img
      src={movie.poster}
      alt={movie.title}
      className="movie-poster"
    />
  ) : (
    <div className="poster-placeholder">
      🎬
    </div>
  )}

  <div className="movie-info">
    <h3>{movie.title}</h3>

    <div className="movie-meta">
      ⭐ {movie.rating} &nbsp; • &nbsp; {movie.release_year}
    </div>

    <p>{movie.overview}</p>
  </div>

</div>
    ))}
  </div>
</section>
        )}
      </main>
      <footer className="footer">
  Built with React, FastAPI & Machine Learning · CineMind
</footer>
    </div>
  );
}

export default App;