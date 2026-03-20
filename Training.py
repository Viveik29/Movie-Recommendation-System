from data_processing import load_data, preprocess_data
from model import vectorize, save_model

# Load data
movies = load_data()

# Preprocess
movies = preprocess_data(movies)

# Vectorize + similarity
vectors, similarity = vectorize(movies)

# Save model
save_model(movies, similarity)

print("✅ Model training completed!")

# Load data
movies = load_data()

# Preprocess
movies = preprocess_data(movies)

# Vectorize + similarity
vectors, similarity = vectorize(movies)

# Save model
save_model(movies, similarity)

print("✅ Model training completed!")