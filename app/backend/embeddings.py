
from sentence_transformers import SentenceTransformer
import numpy as np, streamlit as st

@st.cache_resource
def init_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def embed_texts(texts):
    model = init_model()
    emb = model.encode(list(texts), convert_to_numpy=True, show_progress_bar=False)
    norms = np.linalg.norm(emb, axis=1, keepdims=True) + 1e-10
    return emb / norms
