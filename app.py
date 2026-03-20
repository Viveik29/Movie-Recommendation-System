# # from flask import Flask, render_template, request
# # from routes import routes
# # from recommendation import load_model, recommend

# # app = Flask(__name__)
# # app.register_blueprint(routes)

# # movies, similarity = load_model()


# # @app.route('/', methods=['GET', 'POST'])
# # def home():
# #     recommendations = []
# #     error = None

# #     if request.method == 'POST':
# #         movie = request.form.get('movie')

# #         if not movie:
# #             error = "Please enter a movie name"
# #         else:
# #             recommendations = recommend(movie, movies, similarity)

# #             if not recommendations:
# #                 error = "Movie not found"

# #     return render_template(
# #         'index.html',
# #         recommendations=recommendations,
# #         error=error
# #     )


# # if __name__ == "__main__":
# #     app.run(host="0.0.0.0", port=5000)

# from flask import Flask, render_template, request, jsonify
# from routes import routes
# from recommendation import load_model, recommend
# import logging

# app = Flask(__name__)
# app.register_blueprint(routes)

# # Logging setup
# logging.basicConfig(level=logging.INFO)

# # Load model once
# try:
#     movies, similarity = load_model()
#     logging.info("✅ Model loaded successfully")
# except Exception as e:
#     logging.error(f"❌ Error loading model: {e}")
#     movies, similarity = None, None


# # -----------------------------
# # Input Validation Function
# # -----------------------------
# def validate_input(movie):
#     if not movie:
#         return "Movie name cannot be empty"

#     if len(movie.strip()) < 2:
#         return "Movie name too short"

#     if len(movie) > 100:
#         return "Movie name too long"

#     return None


# # -----------------------------
# # Web UI Route
# # -----------------------------
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     recommendations = []
#     error = None

#     if request.method == 'POST':
#         movie = request.form.get('movie', '').strip()

#         # ✅ Validate input
#         error = validate_input(movie)

#         if not error:
#             try:
#                 if movies is None or similarity is None:
#                     error = "Model not loaded properly"
#                 else:
#                     recommendations = recommend(movie, movies, similarity)

#                     if not recommendations:
#                         error = "Movie not found"

#             except Exception as e:
#                 logging.error(f"Error in recommendation: {e}")
#                 error = "Something went wrong. Please try again."

#     return render_template(
#         'index.html',
#         recommendations=recommendations,
#         error=error
#     )


# # -----------------------------
# # API Endpoint (JSON Response)
# # -----------------------------
# @app.route('/api/recommend', methods=['POST'])
# def api_recommend():
#     try:
#         data = request.get_json()

#         if not data or 'movie' not in data:
#             return jsonify({"error": "Missing 'movie' field"}), 400

#         movie = data['movie'].strip()

#         # Validate input
#         error = validate_input(movie)
#         if error:
#             return jsonify({"error": error}), 400

#         if movies is None or similarity is None:
#             return jsonify({"error": "Model not loaded"}), 500

#         results = recommend(movie, movies, similarity)

#         if not results:
#             return jsonify({"error": "Movie not found"}), 404

#         return jsonify({
#             "status": "success",
#             "movie": movie,
#             "recommendations": results
#         }), 200

#     except Exception as e:
#         logging.error(f"API Error: {e}")
#         return jsonify({"error": "Internal server error"}), 500


# # -----------------------------
# # Global Error Handlers
# # -----------------------------
# @app.errorhandler(404)
# def not_found(e):
#     return render_template('index.html', error="Page not found"), 404


# @app.errorhandler(500)
# def server_error(e):
#     return render_template('index.html', error="Internal server error"), 500


# # -----------------------------
# # Run App
# # -----------------------------
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
from flask import Flask, render_template, request, jsonify
from routes import routes
from recommendation import load_model, recommend
import pandas as pd
import logging

app = Flask(__name__)
app.register_blueprint(routes)

# -----------------------------
# Logging setup
# -----------------------------
logging.basicConfig(level=logging.INFO)

# -----------------------------
# Load ML model
# -----------------------------
try:
    movies, similarity = load_model()
    logging.info("✅ Model loaded successfully")
except Exception as e:
    logging.error(f"❌ Error loading model: {e}")
    movies, similarity = None, None

# -----------------------------
# Load Poster CSV
# -----------------------------
try:
    poster_df = pd.read_csv("movies_with_posters.csv")  # Path to your CSV
    poster_lookup = dict(zip(poster_df['title'], poster_df['poster_url']))
    logging.info("✅ Poster CSV loaded successfully")
except Exception as e:
    logging.error(f"❌ Error loading poster CSV: {e}")
    poster_lookup = {}

# -----------------------------
# Input Validation Function
# -----------------------------
def validate_input(movie):
    if not movie:
        return "Movie name cannot be empty"
    if len(movie.strip()) < 2:
        return "Movie name too short"
    if len(movie) > 100:
        return "Movie name too long"
    return None

# -----------------------------
# Helper: Add posters to recommendations
# -----------------------------
# def recommend_with_posters(movie, movies, similarity):
#     if movie not in movies['title'].values:
#         return []

#     idx = movies[movies['title'] == movie].index[0]
#     sim_scores = list(enumerate(similarity[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]

#     recs = []
#     for i, score in sim_scores:
#         recs.append({
#             "title": movies.iloc[i]['title'],
#             "poster_path": movies.iloc[i]['poster_path'],
#             "rating": movies.iloc[i].get('vote_average', "N/A")  # now include 'rating'
#         })

#     return recs
def recommend_with_posters(movie, movies, similarity):
    movie = movie.strip().lower()

    # Create lowercase column (do once ideally outside function)
    movies['title_lower'] = movies['title'].str.lower()

    # Find matching movie
    matched = movies[movies['title_lower'] == movie]

    if matched.empty:
        return []

    idx = matched.index[0]

    # Get similarity scores
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]

    recs = []
    for i, score in sim_scores:
        recs.append({
            "title": movies.iloc[i]['title'],
            "poster_path": movies.iloc[i]['poster_path'],
            "rating": movies.iloc[i].get('vote_average', "N/A")
        })

    return recs


# -----------------------------
# Web UI Route
# -----------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    error = None

    if request.method == 'POST':
        movie = request.form.get('movie', '').strip().lower()
        error = validate_input(movie.lower())

        if not error:
            try:
                if movies is None or similarity is None:
                    error = "Model not loaded properly"
                else:
                    recommendations = recommend_with_posters(movie, movies, similarity)
                    if not recommendations:
                        error = "Movie not found"

            except Exception as e:
                logging.error(f"Error in recommendation: {e}")
                error = "Something went wrong. Please try again."

    return render_template(
        'index.html',
        recommendations=recommendations,
        error=error
    )

# -----------------------------
# API Endpoint (JSON Response)
# -----------------------------
@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    try:
        data = request.get_json()
        if not data or 'movie' not in data:
            return jsonify({"error": "Missing 'movie' field"}), 400

        movie = data['movie'].strip()
        error = validate_input(movie)
        if error:
            return jsonify({"error": error}), 400

        if movies is None or similarity is None:
            return jsonify({"error": "Model not loaded"}), 500

        results = recommend_with_posters(movie, movies, similarity)
        if not results:
            return jsonify({"error": "Movie not found"}), 404

        return jsonify({
            "status": "success",
            "movie": movie,
            "recommendations": results
        }), 200

    except Exception as e:
        logging.error(f"API Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

# -----------------------------
# Global Error Handlers
# -----------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('index.html', error="Internal server error"), 500

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)