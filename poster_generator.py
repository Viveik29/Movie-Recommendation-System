import pandas as pd
import requests
import time
import os


API_KEY = os.getenv("TMDB_API_KEY")

df = pd.read_csv("tmdb_5000_movies.csv")

def get_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        data = requests.get(url, timeout=5).json()

        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except:
        return None

    return None


# Fetch posters
poster_urls = []

for movie_id in df['id']:
    poster_urls.append(get_poster(movie_id))
    time.sleep(0.2)   # 🔥 avoid rate limit

df['poster_url'] = poster_urls

# Save new CSV
df.to_csv("movies_with_posters.csv", index=False)

print("✅ Done!")