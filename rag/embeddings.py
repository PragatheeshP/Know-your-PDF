from sentence_transformers import (
    SentenceTransformer)
model = SentenceTransformer(
    "BAAI/bge-m3"
)

def embed(texts):

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )
    return embeddings.tolist()