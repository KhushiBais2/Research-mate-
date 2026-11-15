
import faiss
import numpy as np


def create_vector_store(embeddings):

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatIP(dimension)

    # Add embeddings to index
    index.add(embeddings)

    return index


def search_vector_store(index, query_embedding, top_k=3):

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    ).reshape(1, -1)

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    return scores, indices
