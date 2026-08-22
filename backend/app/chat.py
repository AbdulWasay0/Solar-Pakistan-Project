import re

from fastapi import APIRouter

from .llm import generate_answer
from .rag import retrieve_chunks
from .recommend import make_recommendation
from .schemas import ChatRequest, ChatResponse, LoadItem, RecommendationRequest

router = APIRouter()

FALLBACK_ANSWER = "I don't have enough information in the Solar Pakistan knowledge base to answer that."
NON_SOLAR_ANSWER = "I can only answer questions related to solar energy."

SOLAR_TERMS = {
    "solar", "panel", "panels", "photovoltaic", "pv", "inverter", "inverters",
    "battery", "batteries", "on-grid", "ongrid", "off-grid", "offgrid",
    "hybrid", "net-metering", "metering", "nepra", "electricity", "system",
    "systems", "kw", "kwh", "load", "backup", "roof", "pricing", "price",
    "installation", "maintenance", "warranty", "bill", "units", "calculate", "estimate",
    "recommend", "recommendation", "consumption",
}

CITY_NAMES = ["karachi", "lahore", "islamabad", "rawalpindi", "faisalabad", "multan", "peshawar", "hyderabad", "quetta"]
LOAD_WATTS = {
    "ac": 1500,
    "air conditioner": 1500,
    "fan": 80,
    "fans": 80,
    "light": 20,
    "lights": 20,
    "fridge": 250,
    "refrigerator": 250,
    "freezer": 250,
    "pump": 750,
    "motor": 750,
    "washing machine": 500,
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


def _number_before(text: str, labels: list[str]) -> float | None:
    for label in labels:
        match = re.search(rf"(\d+(?:\.\d+)?)\s*(?:{label})", text, re.I)
        if match:
            return float(match.group(1))
        match = re.search(rf"(?:{label})\D{{0,20}}(\d+(?:\.\d+)?)", text, re.I)
        if match:
            return float(match.group(1))
    return None


def _load_items(text: str) -> list[LoadItem]:
    items = []
    for name, watts in LOAD_WATTS.items():
        if name in text:
            match = re.search(rf"(\d+)\s+{re.escape(name)}", text)
            items.append(LoadItem(name=name, watts=watts, quantity=int(match.group(1)) if match else 1))
    return items


def recommendation_from_chat(text: str) -> dict | None:
    lower = text.lower()
    intent = any(word in lower for word in ["calculate", "estimate", "recommend", "sizing", "size my", "solar system"])
    monthly_units = _number_before(lower, ["kwh", "units", "unit", "consumption"])

    if not intent and monthly_units is None:
        return None
    if monthly_units is None or monthly_units <= 0:
        return {
            "answer": (
                "Sure. To calculate your solar system, please send details like:\n\n"
                "City: Islamabad\nMonthly consumption: 650 kWh\nRoof area: 600 sq ft\n"
                "Backup: 4 hours\nBattery: yes/no\nMajor loads: fans, lights, fridge"
            ),
            "topic": "recommendation",
            "sources": ["recommend.py"],
        }

    city = next((c.title() for c in CITY_NAMES if c in lower), None)
    roof_area = _number_before(lower, ["sq ft", "sqft", "roof"] ) or 0
    backup_hours = _number_before(lower, ["hours", "hour", "backup"] ) or 0
    battery_required = "battery" in lower and not re.search(r"battery\s*[:=-]?\s*no", lower)
    preference = "auto"
    if "off-grid" in lower or "off grid" in lower:
        preference = "off-grid"
    elif "on-grid" in lower or "on grid" in lower:
        preference = "on-grid"
    elif "hybrid" in lower:
        preference = "hybrid"

    rec = make_recommendation(RecommendationRequest(
        monthly_units=monthly_units,
        city=city,
        roof_area_sqft=roof_area,
        backup_hours=backup_hours,
        battery_required=battery_required,
        major_loads=_load_items(lower),
        system_preference=preference,
        grid_available=preference != "off-grid",
        panel_watt=585,
    ))
    answer = (
        f"Here is the initial solar recommendation from the sizing engine:\n\n"
        f"- System size: ~{rec['system_kw']} kW\n"
        f"- Panels: ~{rec['panels']} panels of 585W\n"
        f"- Inverter: ~{rec['inverter_kw']} kW\n"
        f"- Battery: ~{rec['battery_kwh']} kWh\n"
        f"- Suggested type: {rec['system_type']}\n\n"
        f"Reason: {rec['reason']}\n\n"
        f"Note: {rec['note']}"
    )
    return {"answer": answer, "topic": "recommendation", "sources": ["recommend.py"]}


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

    history_text = " ".join(item.text for item in data.history[-4:])
    recommendation = recommendation_from_chat(f"{history_text} {question}")
    if recommendation:
        return recommendation

    if not is_solar_question(question) and not has_solar_context(data.history):
        return {"answer": NON_SOLAR_ANSWER, "topic": "general", "sources": []}

    search_question = question
    if data.history:
        search_question = f"{history_text} {question}"

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
