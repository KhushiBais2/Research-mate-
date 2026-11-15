
import ollama


MODEL_NAME = "qwen2.5:3b"


def generate_answer(query, retrieved_chunks):

    if not retrieved_chunks:
        return "No relevant information found in the research paper."

    context = ""

    for i, chunk in enumerate(retrieved_chunks, start=1):
        context += (
            f"\nSource {i} (Page {chunk['page']}):\n"
            f"{chunk['text']}\n"
        )

    prompt = f"""
You are ResearchMate, an AI research paper assistant.

Answer the user's question using only the provided research paper context.

Instructions:
1. Explain concepts in simple and clear language.
2. Do not invent facts or information.
3. If the answer is not available in the context, clearly say so.
4. Mention the relevant page numbers in your answer.
5. Organize the answer using headings or bullet points when useful.

Research Paper Context:
{context}

User Question:
{query}

Answer:
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.2
            }
        )

        return response["message"]["content"]

    except Exception as e:
        return f"Local LLM Error: {str(e)}"
