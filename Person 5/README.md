# Person 5 - README

This folder contains final testing, setup, and deployment deliverables.

## Files
- `TEST_CASES.md` - 32 chatbot test questions
- `TEST_REPORT.md` - verification report
- `SETUP.md` - local run guide
- `DEPLOYMENT.md` - Render/Vercel deployment guide
- `ARCHITECTURE.md` - Mermaid architecture diagram
- `smoke_test.py` - quick API test script

## Before Demo
```powershell
cd backend
python -m app.ingest
python -m uvicorn main:app --reload --port 8000
```

Make sure `backend/.env` has:
```txt
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.6-flash
```

Frontend:
```powershell
cd solar-pakistan-ui-main
npm install
npm run dev
```
