from sentence_transformers import SentenceTransformer
import numpy as np

def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text, model):
    return model.encode([text])[0] 