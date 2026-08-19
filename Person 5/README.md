# Person 5 - README

This folder contains the final testing, documentation, and deployment deliverables.

## Files

- `TEST_CASES.md` - 32 chatbot test questions
- `TEST_REPORT.md` - verification report with results
- `SETUP.md` - full local run commands
- `DEPLOYMENT.md` - deployment plan
- `ARCHITECTURE.md` - Mermaid architecture diagram
- `smoke_test.py` - quick API test script

## Final Project Status

Persons 1-4 are connected in the project. Person 5 adds proof, setup, and deployment docs.

Before demo, run:

```powershell
cd backend
python -m app.ingest
python -m uvicorn main:app --reload --port 8000
```

In another terminal:

```powershell
ollama pull llama3.2:1b
ollama serve
```

In another terminal:

```powershell
cd solar-pakistan-ui-main
npm install
npm run dev
```
