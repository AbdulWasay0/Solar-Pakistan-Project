# Person 5 - Deployment Guide

## Frontend
Recommended: Vercel or Netlify.

Build command:
```txt
npm run build
```

Set this env var if backend is deployed:
```txt
VITE_API_URL=https://your-render-backend.onrender.com
```

## Backend
Recommended: Render free web service.

Start command:
```txt
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Render environment variables:
```txt
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.6-flash
```

## ChromaDB
Current project uses local persisted ChromaDB:
```txt
backend/chroma_db/
```

For Render free, run ingestion during setup/start or later migrate to hosted Chroma/Chroma Cloud.

## LLM
Current project uses Gemini API. It does not use web search. Backend sends only retrieved RAG chunks to Gemini.

## Security
Never commit `.env` or real API keys.
