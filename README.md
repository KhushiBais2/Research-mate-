# ResearchMate – AI-Powered Research Paper Assistant

ResearchMate is an AI-powered research paper assistant built using **Retrieval-Augmented Generation (RAG)**. It allows users to upload research papers in PDF format and ask questions about their content using natural language.

The application retrieves relevant information from the uploaded document and generates context-aware answers using a locally running Large Language Model (LLM).

## Features

- **PDF Upload:** Upload research papers in PDF format.
- **Text Extraction:** Extract text from uploaded research documents.
- **Text Chunking:** Divide extracted text into smaller chunks for efficient retrieval.
- **Semantic Search:** Generate text embeddings using Sentence Transformers.
- **Vector Search:** Store and retrieve relevant chunks using FAISS.
- **AI-Powered Answers:** Generate answers using the Qwen 2.5 model through Ollama.
- **Source Citations:** Display relevant source passages, page numbers and similarity scores.
- **Chat History:** Maintain conversation history during a session.
- **Document Caching:** Avoid reprocessing the same PDF using file hashing.
- **Interactive Dashboard:** User-friendly Streamlit interface.

## Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| Frontend             | Streamlit             |
| PDF Processing       | PyPDF                 |
| Embeddings           | Sentence Transformers |
| Embedding Model      | all-MiniLM-L6-v2      |
| Vector Database      | FAISS                 |
| Large Language Model | Qwen 2.5 (3B)         |
| Local LLM Runtime    | Ollama                |
| Similarity Search    | Cosine Similarity     |

## How It Works

ResearchMate follows a Retrieval-Augmented Generation (RAG) pipeline.

1. **Document Upload:** The user uploads a research paper in PDF format.
2. **Text Extraction:** PyPDF extracts text from the document.
3. **Text Chunking:** The extracted text is divided into smaller overlapping chunks.
4. **Embedding Generation:** Sentence Transformers converts text chunks into numerical vector embeddings.
5. **Vector Storage:** FAISS stores the embeddings for efficient similarity search.
6. **Information Retrieval:** The user's question is converted into an embedding, and FAISS retrieves the most relevant chunks.
7. **Answer Generation:** Retrieved context is passed to the Qwen 2.5 model through Ollama.
8. **Response Display:** ResearchMate displays the generated answer along with relevant source information.

## Project Structure

```text
Research-mate/
│
├── app.py
├── config.py
├── requirement.txt
├── .gitignore
├── sample.pdf
│
├── assets/
│   └── researchmate_logo.png
│
└── src/
    ├── __init__.py
    ├── ingestion.py
    ├── chunking.py
    ├── embeddings.py
    ├── vector_store.py
    ├── retrieval.py
    ├── generation.py
    └── rag_pipeline.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/KhushiBais2/Research-mate-.git
cd Research-mate-
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirement.txt
```

### 5. Install and start Ollama

Download Ollama from:

[https://ollama.com/](https://ollama.com/)

Pull the required model:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running before using the application.

### 6. Run ResearchMate

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## Future Improvements

- Support for multiple research papers.
- Improved document management and persistent chat history.
- Export generated answers and summaries.
- Enhanced retrieval and response evaluation.
- Support for additional language models.

## Author

**Khushi Bais**

GitHub: [https://github.com/KhushiBais2](https://github.com/KhushiBais2)

---

