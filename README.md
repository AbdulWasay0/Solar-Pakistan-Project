# Solar Pakistan RAG Chatbot

An AI-powered solar energy chatbot for Pakistan built with
**Retrieval-Augmented Generation (RAG)**. It retrieves relevant
information from a project knowledge base and uses a locally running
**Ollama** model to generate grounded answers.

## Features

-   Pakistan-focused solar energy question answering
-   Retrieval-Augmented Generation (RAG)
-   FastAPI `/chat` endpoint
-   ChromaDB vector retrieval
-   Local LLM inference with Ollama
-   Sources returned with chatbot responses
-   React + Vite frontend integration
-   Markdown-formatted chatbot responses
-   Filtering of unrelated/non-solar questions
-   Suggested questions in the chatbot UI

## Tech Stack

**Backend:** Python, FastAPI, ChromaDB, Ollama, Uvicorn\
**Frontend:** React, TypeScript, Vite, Tailwind CSS, React Markdown

## Project Structure

``` text
solar-pakistan-rag-chatbot/
├── backend/
│   ├── app/
│   │   ├── ingest.py
│   │   ├── rag.py
│   │   ├── llm.py
│   │   ├── chat.py
│   │   └── ...
│   └── ...
├── Person 1/
├── solar-pakistan-ui-main/
│   ├── src/
│   │   ├── components/
│   │   ├── data/
│   │   ├── lib/
│   │   └── routes/
│   ├── package.json
│   └── ...
└── .gitignore
```

## How It Works

1.  Solar knowledge is prepared and indexed for semantic retrieval.
2.  The user sends a question through the chatbot.
3.  The backend retrieves relevant knowledge chunks.
4.  The retrieved context and question are passed to Ollama.
5.  The model generates an answer based on the retrieved knowledge.
6.  The API returns the answer, topic, and relevant sources.
7.  The React frontend renders the response, including Markdown
    formatting.

## Chat API

### `POST /chat`

Example request:

``` json
{
  "message": "What is a hybrid solar system?"
}
```

Example response:

``` json
{
  "answer": "A hybrid solar system combines solar power, battery storage, and grid power...",
  "topic": "solar",
  "sources": ["faq.md", "pricing.md", "solar_basics.md"]
}
```

For unrelated questions, the chatbot restricts responses to its
solar-energy domain.

## Running the Project

### Backend

``` bash
cd backend
python -m uvicorn app.main:app --reload
```

Install the backend dependencies first and make sure Ollama is installed
and the model configured by the project is available locally.

FastAPI's interactive API documentation can then be accessed through the
local `/docs` route.

### Frontend

``` bash
cd solar-pakistan-ui-main
npm install
npm run dev
```

Open the local URL displayed by Vite.

## Knowledge Base

The chatbot is designed around Solar Pakistan project knowledge covering
areas such as:

-   Solar basics
-   On-grid, off-grid, and hybrid systems
-   Solar pricing
-   Installation
-   Frequently asked questions
-   Solar recommendations

## Git Ignore / Security

The repository excludes common local or generated files:

``` text
__pycache__/
*.pyc
.venv/
venv/
env/
node_modules/
chroma_db/
.env
*.log
```

Do not commit secrets, environment files, generated vector databases, or
`node_modules`.

## Project Status

The main RAG chatbot flow is integrated end-to-end:

-   Knowledge retrieval
-   Ollama answer generation
-   FastAPI chat endpoint
-   Frontend/backend connection
-   Non-solar question filtering
-   Markdown response rendering

## Author

**Taha Ahmad**

Developed as part of the Solar Pakistan AI project/internship work.

## Disclaimer

Solar prices and recommendations can vary with location, equipment,
market conditions, installation requirements, and time. Chatbot
responses should be treated as guidance based on the project's knowledge
base rather than final commercial quotations.
