
from src.embeddings import generate_embeddings
from src.vector_store import search_vector_store


def retrieve_relevant_chunks(
    query,
    index,
    chunks,
    top_k=3
):

    # Generate embedding for user question
    query_embedding = generate_embeddings([
        {
            "text": query,
            "page": 0
        }
    ])

    # Search FAISS database
    scores, indices = search_vector_store(
        index,
        query_embedding,
        top_k
    )

    retrieved_chunks = []

    # Get actual text using retrieved indices
    for i, score in zip(indices[0], scores[0]):

        if i == -1:
            continue

        retrieved_chunks.append({
            "text": chunks[i]["text"],
            "page": chunks[i]["page"],
            "score": float(score)
        })

    return retrieved_chunks
