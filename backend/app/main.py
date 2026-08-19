import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .chat import router as chat_router
from .recommend import make_recommendation
from .schemas import RecommendationRequest, RecommendationResponse

app = FastAPI(title="Solar AI Pakistan API", version="1.0")

allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173", "https://solar-pakistan-project.vercel.app"]
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/knowledge")
def knowledge():
    data = Path(__file__).resolve().parents[1] / "data"
    return [{"topic": f.stem, "source": f.name} for f in sorted(data.glob("*.md"))]


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(data: RecommendationRequest):
    return make_recommendation(data)

