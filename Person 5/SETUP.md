# Person 5 - Setup Guide

## Backend Setup

```powershell
cd "C:\.Me\.Semester 6\Coding\Python\VS Code\Inquisitors\solar-pakistan-rag-chatbot-main\backend"
python -m pip install -r requirements.txt
python -m app.ingest
python -m uvicorn main:app --reload --port 8000
```

## Gemini Setup

Create `backend/.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.6-flash
```

The chatbot does not use Gemini web search. It sends Gemini only the chunks retrieved from the local ChromaDB knowledge base.

## Frontend Setup

Open a second PowerShell window:

```powershell
cd "C:\.Me\.Semester 6\Coding\Python\VS Code\Inquisitors\solar-pakistan-rag-chatbot-main\solar-pakistan-ui-main"
npm install
npm run dev
```

Open the shown local URL, usually `http://localhost:5173`.

## Manual API Tests

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/chat" -ContentType "application/json" -Body '{"message":"What is a hybrid solar system?"}'
```

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/recommend" -ContentType "application/json" -Body '{"monthly_units":600,"city":"Lahore","roof_area_sqft":500,"backup_hours":4,"battery_required":true,"major_loads":[{"name":"Fan","watts":80,"quantity":3}],"system_preference":"auto","grid_available":true,"panel_watt":585}'
```
