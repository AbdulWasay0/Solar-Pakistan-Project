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
    Chunks --> Gemini[Gemini API]
    Gemini --> Chat
    Rec --> Engine[recommend.py Formulas]
    Data[backend/data/*.md] --> Ingest[ingest.py]
    Ingest --> DB
```

## Main Flow

1. Person 1 creates markdown knowledge in `backend/data/`.
2. Person 2 runs `python -m app.ingest` to create `backend/chroma_db/`.
3. Person 3 `/chat` retrieves relevant chunks and sends only those chunks to Gemini.
4. Gemini formats/generates the final answer without web search or tools.
5. Person 4 `/recommend` calculates an initial solar system estimate.
6. Person 5 verifies and documents the system.
