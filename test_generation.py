
from src.generation import generate_answer

retrieved_chunks = [
    {
        "text": "Machine learning is a branch of artificial intelligence "
                "that enables computers to learn from data.",
        "page": 1,
        "score": 0.89
    },
    {
        "text": "Machine learning algorithms identify patterns "
                "and make predictions using training data.",
        "page": 2,
        "score": 0.82
    }
]

query = "What is machine learning?"

answer = generate_answer(
    query,
    retrieved_chunks
)

print("\nResearchMate Answer:")
print(answer)
