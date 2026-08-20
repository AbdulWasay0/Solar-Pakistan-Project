from fastapi import APIRouter

from .llm import generate_answer
from .rag import retrieve_chunks
from .schemas import ChatRequest, ChatResponse

router = APIRouter()

FALLBACK_ANSWER = "I don't have enough information in the Solar Pakistan knowledge base to answer that."
NON_SOLAR_ANSWER = "I can only answer questions related to solar energy."

SOLAR_TERMS = {
    "solar", "panel", "panels", "photovoltaic", "pv", "inverter", "inverters",
    "battery", "batteries", "on-grid", "ongrid", "off-grid", "offgrid",
    "hybrid", "net-metering", "metering", "nepra", "electricity", "system",
    "systems", "kw", "kwh", "load", "backup", "roof", "pricing", "price",
    "installation", "maintenance", "warranty", "bill", "units", "calculate",
}


def is_greeting(question: str) -> bool:
    normalized = question.lower().strip(" .,!?0123456789")
    greetings = {"hi", "hello", "hey", "salam", "assalamualaikum", "assalamu alaikum"}
    return normalized in greetings


def normalized_words(text: str) -> set[str]:
    cleaned = text.lower()
    for char in "?.,/:;()[]{}-_":
        cleaned = cleaned.replace(char, " ")
    return set(cleaned.split())


def is_solar_question(question: str) -> bool:
    return bool(normalized_words(question).intersection(SOLAR_TERMS))


def has_solar_context(history) -> bool:
    recent = " ".join(item.text for item in history[-6:])
    return is_solar_question(recent)


@router.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest):
    question = data.message.strip()

    if not question:
        return {"answer": FALLBACK_ANSWER, "topic": "general", "sources": []}

    if is_greeting(question):
        return {
            "answer": "Hi! Ask me anything about solar panels, inverters, batteries, pricing, installation, net metering, or system sizing in Pakistan.",
            "topic": "general",
            "sources": [],
        }

    if not is_solar_question(question) and not has_solar_context(data.history):
        return {"answer": NON_SOLAR_ANSWER, "topic": "general", "sources": []}

    search_question = question
    if data.history:
        recent_context = " ".join(item.text for item in data.history[-4:])
        search_question = f"{recent_context} {question}"

    chunks = retrieve_chunks(search_question)
    if not chunks:
        return {"answer": FALLBACK_ANSWER, "topic": "solar", "sources": []}

    answer = generate_answer(search_question, chunks).strip()
    if answer == FALLBACK_ANSWER:
        return {"answer": FALLBACK_ANSWER, "topic": "solar", "sources": []}

    sources = []
    for chunk in chunks:
        source = chunk.get("source")
        if source and source != "unknown" and source not in sources:
            sources.append(source)

    return {"answer": answer, "topic": "solar", "sources": sources}
