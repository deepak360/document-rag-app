##  Concept used with this project

-   cosine_similarity
-   Langchain / OpenAI / HuggingFace
-   TfidfVectorizer

- Why SentenceTransformer("all-MiniLM-L6-v2") — Can We Do Better?
✅ Pros:

    Small and fast (80MB)

    Great for quick prototyping and short texts

    Well supported by sentence-transformers

    Works well for chunking-based RAG

❌ Limitations:

    Lower semantic understanding on long/formal documents

    Not ideal for code, medical, or legal domains

🚀 Better Models You Can Try
🔹 1. BAAI/bge-small-en-v1.5

    Smaller than MiniLM, but performs better on search tasks

    Recommended by OpenAI and LangChain for RAG

```
SentenceTransformer("BAAI/bge-small-en-v1.5")
```