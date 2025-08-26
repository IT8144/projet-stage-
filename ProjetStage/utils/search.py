import numpy as np

def search(query_embedding, doc_embeddings, top_k=3):
    # Normalisation
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    doc_norms = doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
    similarities = np.dot(doc_norms, query_norm)
    top_indices = similarities.argsort()[-top_k:][::-1]
    return top_indices 