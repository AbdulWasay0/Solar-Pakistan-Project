# Person 5 - Architecture Diagram

```mermaid
flowchart TD
    U[User] --> F[React Frontend]
    F --> C[Chat Widget]
    C --> API[FastAPI Backend]
    API --> Health[/health]
    API --> Chat[/chat]
    API --> Rec[/recommend]
    Chat --> RAG[rag.py]
    RAG --> KB[knowledge.py]
    KB --> DB[(Local ChromaDB: backend/chroma_db)]
    DB --> Chunks[Retrieved Top 3 Chunks]
    Chunks --> LLM[Ollama llama3.2:1b]
    LLM --> Chat
    Rec --> Engine[recommend.py Formulas]
    Data[backend/data/*.md] --> Ingest[ingest.py]
    Ingest --> DB
```

## Main Flow

1. Person 1 creates markdown knowledge in `backend/data/`.
2. Person 2 runs `python -m app.ingest` to create `backend/chroma_db/`.
3. Person 3 `/chat` retrieves relevant chunks and sends them to Ollama.
4. Person 4 `/recommend` calculates an initial solar system estimate.
5. Frontend calls backend endpoints from the chat/calculator UI.
