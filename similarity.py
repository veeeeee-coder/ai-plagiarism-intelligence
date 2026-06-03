from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai import Credentials
import numpy as np
import pickle
from config import API_KEY, PROJECT_ID

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_top_matches(query_text, top_k=3):
    credentials = Credentials(
        url="https://au-syd.ml.cloud.ibm.com",
        api_key=API_KEY
    )
    
    embedding_model = Embeddings(
        model_id="ibm/slate-30m-english-rtrvr-v2",
        credentials=credentials,
        project_id=PROJECT_ID
    )
    
    with open('data/vector_store.pkl', 'rb') as f:
        df = pickle.load(f)
    
    query_vec = embedding_model.embed_documents(texts=[query_text])[0]
    
    scores = []
    for _, row in df.iterrows():
        score = cosine_similarity(query_vec, row['vector'])
        scores.append({
            'text': row['text'][:200],
            'label': row['label'],
            'score': round(float(score), 4)
        })
    
    scores.sort(key=lambda x: -x['score'])
    return scores[:top_k]