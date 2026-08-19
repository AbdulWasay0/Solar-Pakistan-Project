# Person 5 - Deployment Guide

## Frontend

Recommended: Vercel or Netlify.

Build command:

```txt
npm run build
```

Publish/build folder depends on TanStack Start output. Verify with the frontend README/build output before deployment.

## Backend

Recommended: Render, Railway, or Fly.io.

Start command:

```txt
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Before deployment, run ingestion once so `backend/chroma_db/` exists, or upload/preserve it as persistent storage.

## ChromaDB

Current project uses local persisted ChromaDB:

```txt
backend/chroma_db/
```

For production, either:

- use persistent disk on Render/Railway/Fly.io, or
- migrate later to hosted Chroma/Chroma Cloud.

## LLM

Current project uses local Ollama:

```txt
http://localhost:11434/api/generate
```

For production, replace Ollama with OpenAI/Gemini or deploy Ollama on the same server/private network.

## Environment Notes

Never commit real API keys or `.env` files. Keep generated folders out of Git unless intentionally needed for demo deployment.
