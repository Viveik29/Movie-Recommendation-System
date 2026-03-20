import pandas as pd
import ast

# -------------------------------
# Load Data
# -------------------------------
def load_data():
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")

    movies = movies.merge(credits, on='title')
    return movies


# -------------------------------
# Helper Functions
# -------------------------------
def convert(text):
    """Convert string list of dict to list of names"""
    try:
        return [i['name'] for i in ast.literal_eval(text)]
    except:
        return []


def convert_cast(text):
    """Take top 3 cast only"""
    try:
        return [i['name'] for i in ast.literal_eval(text)[:3]]
    except:
        return []


def fetch_director(text):
    """Extract director from crew"""
    try:
        crew_list = ast.literal_eval(text)
        for i in crew_list:
            if i['job'] == 'Director':
                return [i['name']]
        return []
    except:
        return []


def clean_text(text_list):
    """Remove spaces (important for NLP)"""
    return [i.replace(" ", "") for i in text_list]


# -------------------------------
# Preprocessing
# -------------------------------
def preprocess_data(movies):

    # Keep required columns (IMPORTANT: add rating + popularity)
    movies = movies[['id','title','overview','genres','keywords','cast','crew',
                     'vote_average','popularity']]

    movies.rename(columns={'id': 'movie_id'}, inplace=True)

    # Drop missing
    movies.dropna(inplace=True)

    # Convert columns
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert_cast)
    movies['crew'] = movies['crew'].apply(fetch_director)

    # Clean text (remove spaces)
    movies['genres'] = movies['genres'].apply(clean_text)
    movies['keywords'] = movies['keywords'].apply(clean_text)
    movies['cast'] = movies['cast'].apply(clean_text)
    movies['crew'] = movies['crew'].apply(clean_text)

    # Overview → split words
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    # 🔥 Create TAGS (Main ML Feature)
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

    # Convert list → string
    movies['tags'] = movies['tags'].apply(lambda x: " ".join(x).lower())

    return movies[['movie_id', 'title', 'tags', 'genres', 'vote_average', 'popularity']]

# import pandas as pd

# def load_data():
#     movies = pd.read_csv("tmdb_5000_movies.csv")
#     credits = pd.read_csv("tmdb_5000_credits.csv")

#     movies = movies.merge(credits, on='title')
#     return movies


# def preprocess_data(movies):
#     movies['genres'] = movies['genres'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)])
#     movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
#     movies.dropna(inplace=True)

#     return movies
# import pandas as pd
# import ast
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()
# TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# # -------------------------------
# # Load Data
# # -------------------------------
# def load_data():
#     movies = pd.read_csv("tmdb_5000_movies.csv")
#     credits = pd.read_csv("tmdb_5000_credits.csv")
#     movies = movies.merge(credits, on='title')
#     return movies

# # -------------------------------
# # Helper Functions
# # -------------------------------
# def convert(text):
#     try:
#         return [i['name'] for i in ast.literal_eval(text)]
#     except:
#         return []

# def convert_cast(text):
#     try:
#         return [i['name'] for i in ast.literal_eval(text)[:3]]
#     except:
#         return []

# def fetch_director(text):
#     try:
#         crew_list = ast.literal_eval(text)
#         for i in crew_list:
#             if i['job'] == 'Director':
#                 return [i['name']]
#         return []
#     except:
#         return []

# def clean_text(text_list):
#     return [i.replace(" ", "") for i in text_list]

# # -------------------------------
# # Fetch Poster Path Once
# # -------------------------------
# def fetch_poster_path(movie_id):
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
#         data = requests.get(url).json()
#         return data.get("poster_path")
#     except:
#         return None

# # -------------------------------
# # Preprocessing
# # -------------------------------
# def preprocess_data(movies):
#     movies = movies[['id','title','overview','genres','keywords','cast','crew',
#                      'vote_average','popularity']]
#     movies.rename(columns={'id': 'movie_id'}, inplace=True)
#     movies.dropna(inplace=True)

#     movies['genres'] = movies['genres'].apply(convert)
#     movies['keywords'] = movies['keywords'].apply(convert)
#     movies['cast'] = movies['cast'].apply(convert_cast)
#     movies['crew'] = movies['crew'].apply(fetch_director)

#     movies['genres'] = movies['genres'].apply(clean_text)
#     movies['keywords'] = movies['keywords'].apply(clean_text)
#     movies['cast'] = movies['cast'].apply(clean_text)
#     movies['crew'] = movies['crew'].apply(clean_text)

#     movies['overview'] = movies['overview'].apply(lambda x: x.split())
#     movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
#     #movies['tags'] = movies['tags'].apply(lambda x: " ".join(x).lower())
#     movies = movies.copy()   # make a full copy before modifying
#     movies.loc[:, 'tags'] = movies['tags'].apply(lambda x: " ".join(x).lower())

#     # ✅ Add poster_path column
#     movies['poster_path'] = movies['movie_id'].apply(fetch_poster_path)

#     return movies[['movie_id', 'title', 'tags', 'genres', 'vote_average', 'popularity', 'poster_path']]