from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
from utils.extract import extract_text_from_pdf
from utils.embed import get_embedding, load_model
from utils.search import search
import numpy as np
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

DATA_DIR = 'data'
EMBEDDINGS_FILE = 'embeddings/embeddings.npy'
TEXTS_FILE = 'embeddings/texts.npy'

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs('embeddings', exist_ok=True)

# Chargement du modèle d'embeddings
model = load_model()

@app.post('/upload')
def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    return {"filename": file.filename}

@app.post('/index')
def index_documents():
    texts = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(os.path.join(DATA_DIR, filename))
            texts.append(text)
    # Découpage en paragraphes
    chunks = [p for text in texts for p in text.split('\n') if len(p.strip()) > 30]
    embeddings = np.array([get_embedding(chunk, model) for chunk in chunks])
    np.save(EMBEDDINGS_FILE, embeddings)
    np.save(TEXTS_FILE, np.array(chunks))
    return {"status": "Indexation terminée", "chunks": len(chunks)}

@app.post('/chat')
def chat(question: str = Form(...)):
    import openai
    openai.api_key = "sk-..."  # Remplace par ta vraie clé API OpenAI
    try:
        # Charger embeddings et textes
        embeddings = np.load(EMBEDDINGS_FILE)
        texts = np.load(TEXTS_FILE, allow_pickle=True)
        # Embedding de la question
        q_emb = get_embedding(question, model)
        idxs = search(q_emb, embeddings, top_k=3)
        context = '\n'.join([texts[i] for i in idxs]) if len(idxs) > 0 else ''
        # Génération de la réponse (OpenAI)
        if context.strip():
            prompt = f"Voici des informations sur l'entreprise :\n{context}\n\nQuestion : {question}\nRéponse :"
        else:
            prompt = f"Question : {question}\nRéponse :"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        return JSONResponse({"answer": response.choices[0].text.strip()})
    except Exception as e:
        return JSONResponse({"answer": f"Erreur serveur : {str(e)}"}, status_code=500)

@app.post('/testchat')
def testchat(question: str = Form(...)):
    return {"answer": f"Tu as demandé : {question}"}