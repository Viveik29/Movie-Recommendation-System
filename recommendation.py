import requests
from dotenv import load_dotenv
import os
import pickle
import pandas as pd


#TMDB_API_KEY = os.getenv["TMDB_API_KEY"]
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        data = requests.get(url).json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

        return "https://via.placeholder.com/500x750?text=No+Image"

    except Exception as e:
        print("Error fetching poster:", e)
        return "https://via.placeholder.com/500x750?text=Error"

# def load_model():
#     movies = pickle.load(open('models/movie_list.pkl', 'rb'))
#     similarity = pickle.load(open('models/similarity.pkl', 'rb'))

    
#     return movies, similarity


# import pandas as pd
# import pickle

import pickle
import pandas as pd

# def load_model():
#     # Load original movie data
#     movies = pickle.load(open('models/movie_list.pkl', 'rb'))
#     similarity = pickle.load(open('models/similarity.pkl', 'rb'))

#     # Load poster CSV
#     posters = pd.read_csv('movies_with_posters.csv')

#     # Strip spaces in titles
#     movies['title'] = movies['title'].str.strip()
#     posters['title'] = posters['title'].str.strip()

#     # Merge only title + poster_url
#     movies = movies.merge(posters[['title', 'poster_url']], on='title', how='left')

#     # Create poster_path column for backend
#     movies['poster_path'] = movies['poster_url'].fillna(
#         "https://via.placeholder.com/500x750?text=No+Image"
#     )

#     return movies, similarity
import pickle
import pandas as pd

def load_model():
    # Load movie list and similarity
    movies = pickle.load(open('models/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('models/similarity.pkl', 'rb'))

    # Load poster CSV
    posters = pd.read_csv('movies_with_posters.csv')

    # Strip titles
    movies['title'] = movies['title'].str.strip()
    posters['title'] = posters['title'].str.strip()

    # Merge title + poster_url
    movies = movies.merge(posters[['title', 'poster_url']], on='title', how='left')

    # Handle relative TMDB paths (if poster_url starts with /)
    TMDB_BASE = "https://image.tmdb.org/t/p/w500"
    movies['poster_path'] = movies['poster_url'].apply(
        lambda x: TMDB_BASE + x if pd.notnull(x) and x.startswith('/') else (x if pd.notnull(x) else "https://via.placeholder.com/500x750?text=No+Image")
    )

    return movies, similarity


def recommend(movie, movies, similarity):
    movie = movie.lower()

    if movie not in movies['title'].str.lower().values:
        return []

    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))

    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:20]

    rec_df = movies.iloc[[i[0] for i in movies_list]]

    # 🔥 sort by rating
    rec_df = rec_df.sort_values(by='vote_average', ascending=False)

    results = []

    for _, row in rec_df.head(5).iterrows():
        results.append({
            "title": row['title'],
            "rating": float(row['vote_average']),
            "popularity": float(row['popularity']),
            "genres": ", ".join(row['genres']) if isinstance(row['genres'], list) else row['genres'],
            "poster": fetch_poster(row['movie_id'])
        })

    return results