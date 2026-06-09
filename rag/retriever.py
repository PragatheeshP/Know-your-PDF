print("=== RETRIEVER VERSION 2 LOADED ===")
from rag.vector_store import (
    client,
    COLLECTION_NAME
)

def search(query_vector, limit=5):
    print("=== USING QUERY_POINTS ===")

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )

    return results.points