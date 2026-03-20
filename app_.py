from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load data
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movies = movies.reset_index(drop=True)
movies['title_lower'] = movies['title'].str.lower()


def recommend(movie):
    movie = movie.lower()
    if movie not in movies['title_lower'].values:
        return []

    index = movies[movies['title_lower'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])

    recommended_movies = []
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    if request.method == 'POST':
        movie = request.form['movie']
        recommendations = recommend(movie)
    return render_template('index.html', recommendations=recommendations)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

