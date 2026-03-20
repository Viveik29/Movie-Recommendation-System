from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


def vectorize(movies):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()

    similarity = cosine_similarity(vectors)

    return vectors, similarity


def save_model(movies, similarity):
    pickle.dump(movies, open('models/movie_list.pkl', 'wb'))
    pickle.dump(similarity, open('models/similarity.pkl', 'wb'))