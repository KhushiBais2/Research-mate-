
from src.ingestion import extract_text_from_pdf
from src.chunking import create_chunks
from src.embeddings import generate_embeddings
from src.vector_store import create_vector_store
from src.retrieval import retrieve_relevant_chunks
from src.generation import generate_answer


def process_document(pdf_path):

    print("Extracting text from PDF...")
    pages = extract_text_from_pdf(pdf_path)

    if not pages:
        raise ValueError("No readable text found in the PDF.")

    print("Creating text chunks...")
    chunks = create_chunks(pages)

    if not chunks:
        raise ValueError("No text chunks were created.")

    print("Generating embeddings...")
    embeddings = generate_embeddings(chunks)

    print("Creating FAISS vector database...")
    index = create_vector_store(embeddings)

    print("Document processing completed!")

    return index, chunks


def answer_question(query, index, chunks, top_k=3):

    print("Retrieving relevant information...")

    retrieved_chunks = retrieve_relevant_chunks(
        query,
        index,
        chunks,
        top_k=top_k
    )

    print("Generating answer using Qwen...")

    answer = generate_answer(query, retrieved_chunks)

    return answer, retrieved_chunks


# Backward-compatible function for existing tests
def process_research_paper(pdf_path, query, top_k=3):

    index, chunks = process_document(pdf_path)

    return answer_question(
        query,
        index,
        chunks,
        top_k=top_k
    )
