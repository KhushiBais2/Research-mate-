
from src.rag_pipeline import process_research_paper

pdf_path = "sample.pdf"

query = input("Ask a question about your research paper: ")

answer, sources = process_research_paper(
    pdf_path,
    query
)

print("\n========== ResearchMate Answer ==========")
print(answer)

print("\n========== Retrieved Sources ==========")

for source in sources:
    print("\nPage:", source["page"])
    print("Similarity Score:", round(source["score"], 3))
    print("Text:", source["text"][:300])

