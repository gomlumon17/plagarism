import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def tfidf_sim(a, b):
    try:
        vec = TfidfVectorizer().fit_transform([a, b])
        return float(cosine_similarity(vec[0:1], vec[1:2])[0][0])
    except:
        return 0.0

def jaccard_sim(a, b):
    wa = set(a.lower().split())
    wb = set(b.lower().split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)

def embedding_matrix(chunks1, chunks2):
    e1 = model.encode(chunks1, convert_to_numpy=True, normalize_embeddings=True)
    e2 = model.encode(chunks2, convert_to_numpy=True, normalize_embeddings=True)
    return np.dot(e1, e2.T)

def final_score(tfidf_score, jaccard_score, embedding_score):
    return 0.25 * tfidf_score + 0.15 * jaccard_score + 0.60 * embedding_score