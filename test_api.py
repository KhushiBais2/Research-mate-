import ollama

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain machine learning in simple language."
        }
    ]
)

print("\nResearchMate Local LLM Response:")
print(response["message"]["content"])