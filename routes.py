from flask import Blueprint, request, jsonify
from recommendation import load_model, recommend

routes = Blueprint('routes', __name__)

movies, similarity = load_model()


@routes.route('/recommend', methods=['POST'])
def recommend_movies():
    try:
        data = request.json
        movie = data.get('movie')

        if not movie:
            return jsonify({"error": "Movie name required"}), 400

        result = recommend(movie, movies, similarity)

        return jsonify({"recommendations": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route('/health', methods=['GET'])
def health():
    return {"status": "running"}