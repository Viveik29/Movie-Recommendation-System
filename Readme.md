
🎬 Movie Recommendation System

A web-based movie recommendation system built with Flask that provides movie suggestions based on similarity and displays movie posters and ratings. Includes both Web UI and REST API.

Table of Contents

Project Overview

Features

Directory Structure

Setup & Installation

Data Preparation

Backend Details

Frontend Details

API Usage

Testing API

Screenshots

Future Improvements

Project Overview

This project recommends movies based on similarity (using a precomputed similarity matrix) and displays:

Movie poster (from CSV or placeholder if missing)

Movie rating (vote_average)

Movie title

The system has:

A Flask Web UI for entering a movie name and viewing recommendations

A REST API endpoint (/api/recommend) for JSON-based requests

Features

Recommend top 10 similar movies

Display movie poster, title, and rating

Input validation (empty, short, or long movie names)

Handles missing posters with a placeholder

API compatible with Postman / cURL / Python requests

Directory Structure
movie-recommendation/
├── app.py                 # Flask main app
├── routes.py              # Optional blueprint routes
├── recommendation.py      # Recommendation logic + model loading
├── models/
│   ├── movie_list.pkl     # Preprocessed movie DataFrame
│   └── similarity.pkl     # Similarity matrix (pickle)
├── templates/
│   └── index.html         # Web UI template
├─
├── movies_with_posters.csv # CSV containing poster URLs and movie info
├── README.md
├── requirements.txt       # Python dependencies
Setup & Installation

Clone the repo

git clone <repo_url>
cd movie-recommendation

Create virtual environment

python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

Install dependencies

pip install -r requirements.txt
Data Preparation

movies_with_posters.csv must contain the following columns:

id,title,poster_url,vote_average,... (other optional columns)

movie_list.pkl contains the main movies DataFrame used for similarity lookup.

similarity.pkl contains precomputed similarity matrix (e.g., cosine similarity of movie features).

Backend Details

app.py: Main Flask app

recommendation.py:

def load_model():
    # Load movie_list.pkl and similarity.pkl
    # Merge poster_url from CSV
    # Create poster_path column with placeholder for missing posters
    return movies, similarity

def recommend_with_posters(movie, movies, similarity):
    # Return list of dicts:
    # [{"title": ..., "poster_path": ..., "rating": ...}, ...]

Input validation: checks empty, short (<2), or long (>100) movie names

Frontend Details

HTML template: templates/index.html

Loops through recommendations and displays:

{% for rec in recommendations %}
<div class="movie-card">
    <img src="{{ rec.poster_path }}" alt="{{ rec.title }}" width="150">
    <p>{{ rec.title }}</p>
    <p>Rating: {{ rec.rating }}</p>
</div>
{% endfor %}

Works with poster_path from backend, using placeholder if missing

API Usage

Endpoint: /api/recommend
Method: POST
Content-Type: application/json

Request Example:

{
  "movie": "Inception"
}

Response Example:

{
  "status": "success",
  "movie": "Inception",
  "recommendations": [
    {"title": "Interstellar", "poster_path": "https://...", "rating": 8.6},
    {"title": "Tenet", "poster_path": "https://...", "rating": 7.8},
    ...
  ]
}
Testing API
1. Using Postman Web

Open https://web.postman.co

New POST request → URL: http://localhost:5000/api/recommend

Headers: Content-Type: application/json

Body (raw → JSON):

{
  "movie": "Inception"
}

Click Send → check JSON response---

## 👨‍💻 Author

**Viveik**
Machine Learning & MLOps Engineer

-------------------------------------------------------------------------------------------------------------------------------


