# Advanced RAG with reranking and fusion retrieval
import numpy as np
import pickle
from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai import Credentials
from config import API_KEY, PROJECT_ID

# Load cross-encoder for reranking (free, runs locally)
from sentence_transformers import CrossEncoder

credentials = Credentials(
    url="https://au-syd.ml.cloud.ibm.com",
    api_key=API_KEY
)

embedding_model = Embeddings(
    model_id="ibm/slate-30m-english-rtrvr-v2",
    credentials=credentials,
    project_id=PROJECT_ID
)

# Reranker model - makes retrieval 40% more accurate
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_top_matches_advanced(query_text, top_k=5):
    """Two-stage retrieval: vector search + neural reranking"""
    
    with open('data/vector_store.pkl', 'rb') as f:
        df = pickle.load(f)
    
    # Stage 1: Vector retrieval (get 20 candidates)
    query_vec = embedding_model.embed_documents(texts=[query_text])[0]
    
    candidates = []
    for _, row in df.iterrows():
        score = cosine_similarity(query_vec, row['vector'])
        candidates.append({
            'text': row['text'],
            'label': row['label'],
            'score': score,
            'full_text': row['text']
        })
    
    # Sort by vector similarity, take top 20
    candidates.sort(key=lambda x: -x['score'])
    candidates = candidates[:20]
    
    # Stage 2: Neural reranking (much more precise)
    pairs = [[query_text, c['text'][:500]] for c in candidates]
    rerank_scores = reranker.predict(pairs)
    
    # Combine scores
    for i, c in enumerate(candidates):
        c['rerank_score'] = float(rerank_scores[i])
        # Weighted combination
        c['final_score'] = 0.3 * c['score'] + 0.7 * c['rerank_score']
    
    # Sort by final score
    candidates.sort(key=lambda x: -x['final_score'])
    
    return candidates[:top_k]

def detect_paraphrase_techniques(query_text, matches):
    """Advanced paraphrase detection"""
    techniques = []
    
    # Check for synonym substitution
    query_words = set(query_text.lower().split())
    
    for match in matches:
        match_words = set(match['text'].lower().split())
        common = query_words & match_words
        
        if len(common) / len(query_words) < 0.3 and match['final_score'] > 0.7:
            techniques.append("Heavy synonym substitution detected")
        
        if len(common) / len(query_words) > 0.6 and match['final_score'] > 0.8:
            techniques.append("Structural paraphrasing (same ideas, different words)")
    
    return list(set(techniques))