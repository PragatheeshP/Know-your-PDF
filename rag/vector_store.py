from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)
COLLECTION_NAME = "documents"

client = QdrantClient(
    host="localhost",
    port=6333
)
def create_collection():
    collections = [
        c.name
        for c in client.get_collections().collections
    ]
    if COLLECTION_NAME not in collections:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

def insert_chunks(chunks, embeddings):

    points = []

    for idx, (chunk, vector) in enumerate(
        zip(chunks, embeddings)
    ):
        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "text": chunk["text"],
                    "page": chunk["page"]
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )