from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings
import pickle
import pandas as pd
from config import API_KEY, PROJECT_ID

print("🔄 Loading IBM embedding model...")

credentials = Credentials(
    url="https://au-syd.ml.cloud.ibm.com",
    api_key=API_KEY
)

print(f"API Key loaded: {'YES' if API_KEY else 'NO'}")
print(f"Project ID: {PROJECT_ID}")

embedding_model = Embeddings(
    model_id="ibm/slate-30m-english-rtrvr-v2",
    credentials=credentials,
    project_id=PROJECT_ID
)

df = pd.read_csv('data/dataset.csv')
texts = df['text'].tolist()

print(f"📚 Embedding {len(texts)} documents...")

vectors = []
batch_size = 3

for i in range(0, len(texts), batch_size):
    batch = texts[i:i + batch_size]
    print(f"  Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}...")
    result = embedding_model.embed_documents(texts=batch)
    vectors.extend(result)

df['vector'] = vectors
with open('data/vector_store.pkl', 'wb') as f:
    pickle.dump(df, f)

print(f"✅ Vector store saved! {len(vectors)} documents embedded.")