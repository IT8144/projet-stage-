# Chatbot Entreprise (Projet de Stage)

Ce projet est un chatbot intelligent capable de répondre aux questions sur une entreprise en se basant sur les documents fournis (PDF, Word, etc.).

## Fonctionnalités principales
- Upload de documents
- Extraction de texte
- Indexation sémantique (embeddings)
- Recherche intelligente
- Génération de réponses contextuelles

## Stack technique
- Python, FastAPI
- pdfplumber, sentence-transformers
- OpenAI ou modèle open-source

## Lancement rapide
1. Placez vos documents dans le dossier `data/`
2. Installez les dépendances : `pip install -r requirements.txt`
3. Lancez l'API : `uvicorn app:app --reload`

---

Ce projet est un point de départ, à adapter selon vos besoins ! 

---

## Solution immédiate : Corriger le montage des fichiers statiques

**Le problème vient probablement de cette ligne dans ton code :**
```python
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```
Quand tu montes les fichiers statiques sur `/`, cela **écrase toutes les routes API** (POST `/chat`, `/testchat`, etc.) pour les requêtes POST, car FastAPI ne fait plus la différence entre les routes API et les fichiers statiques.

---

### **Correction à faire :**

**Remplace cette ligne :**
```python
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```
**par :**
```python
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
```

- Cela sert les fichiers statiques sur `/static` au lieu de `/` et laisse toutes les routes API fonctionner normalement.

---

### **Étapes à suivre :**

1. Modifie la ligne comme indiqué ci-dessus dans `app.py`.
2. Redémarre le serveur :
   ```
   uvicorn app:app --reload
   ```
3. Va sur [http://localhost:8000/docs](http://localhost:8000/docs)
4. Teste à nouveau **POST /testchat** et **POST /chat**.

---

**Dis-moi si ça fonctionne après cette modification !  
C’est une cause classique de 405 sur toutes les routes POST dans FastAPI.** 