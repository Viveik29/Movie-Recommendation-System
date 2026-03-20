
# 🎬 Movie Recommender System (Flask + ML + Docker)

A content-based movie recommendation system built using **Machine Learning (NLP)** and deployed with **Flask & Docker**.
It suggests similar movies based on user input using cosine similarity.

---

## 🚀 Features

* 🔍 Search any movie and get top 5 recommendations
* 🧠 Content-based filtering using NLP (CountVectorizer)
* ⚡ Fast similarity computation using cosine similarity
* 🌐 Interactive UI using HTML/CSS
* 🐳 Dockerized for easy deployment
* 🔐 Environment-based configuration using `.env`

---

## 🧠 How It Works

1. Movie data is preprocessed and combined into a `tags` column
2. Text data is vectorized using **CountVectorizer**
3. Cosine similarity is computed between all movies
4. Based on input movie, similar movies are recommended

---

## 📂 Project Structure

```
movie-recommender/
│
├── app.py
├── movie_list.pkl
├── similarity.pkl
├── requirements.txt
├── Dockerfile
├── .env
├── .gitignore
│
└── templates/
    └── index.html
```

---

## ⚙️ Installation (Local Setup)

### 1. Create environment (Recommended: Conda)

```
conda create -n movie-reco python=3.10 -y
conda activate movie-reco
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the app

```
python app.py
```

### 4. Open in browser

```
http://localhost:5000
```

---

## 🐳 Docker Setup

### 1. Build Docker Image

```
docker build -t movie-recommender .
```

### 2. Run Container

```
docker run -p 5001:5000 movie-recommender
```

### 3. Open in browser

```
http://localhost:5001
```

---

## ☁️ Push to Docker Hub

```
docker tag movie-recommender <your-username>/movie-recommender:latest
docker push <your-username>/movie-recommender:latest
```

---

## 🔐 Environment Variables

Create a `.env` file:

```
FLASK_ENV=development
SECRET_KEY=your_secret_key
PORT=5000
```

---

## 📊 Tech Stack

* **Python**
* **Flask**
* **Scikit-learn**
* **Pandas**
* **NLP (CountVectorizer)**
* **Docker**

---

## 🎯 Future Improvements

* 🎬 Add movie posters (TMDB API)
* 🔍 Autocomplete search
* ⭐ Show ratings & metadata
* 🤖 Upgrade to GenAI-based recommendations (RAG + LLM)
* ☁️ Deploy on AWS / Kubernetes

---

## 🧠 Learnings

* Built end-to-end ML pipeline
* Implemented cosine similarity for recommendations
* Containerized application using Docker
* Learned deployment and environment management

---

## 👨‍💻 Author

**Viveik**
Machine Learning & MLOps Engineer

-------------------------------------------------------------------------------------------------------------------------------


