from fastapi import APIRouter
from .schemas import ChatRequest, ChatResponse
from .rag import retrieve_chunks
from .llm import generate_answer


router = APIRouter()

FALLBACK_ANSWER = (
    "I don't have enough information in the Solar Pakistan "
    "knowledge base to answer that."
)

NON_SOLAR_ANSWER = (
    "I can only answer questions related to solar energy."
)


# Words that strongly indicate that the question belongs
# to the Solar Pakistan assistant's domain.
SOLAR_TERMS = {
    "solar",
    "panel",
    "panels",
    "photovoltaic",
    "pv",
    "inverter",
    "inverters",
    "battery",
    "batteries",
    "on-grid",
    "ongrid",
    "off-grid",
    "offgrid",
    "hybrid",
    "net-metering",
    "metering",
    "nepra",
    "electricity",
    "system",
    "systems",
    "kw",
    "kwh",
    "load",
    "backup",
    "roof",
}


def is_solar_question(question: str) -> bool:
    """
    Basic domain guard.

    Prevent completely unrelated questions from being sent
    through the solar RAG pipeline.
    """

    normalized = (
        question.lower()
        .replace("?", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace("/", " ")
    )

    words = set(normalized.split())

    return bool(words.intersection(SOLAR_TERMS))


@router.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest):

    question = data.message.strip()

    # ---------------------------------------------------------
    # 1. Reject empty questions
    # ---------------------------------------------------------

    if not question:
        return {
            "answer": FALLBACK_ANSWER,
            "topic": "general",
            "sources": [],
        }

    # ---------------------------------------------------------
    # 2. Reject clearly non-solar questions BEFORE retrieval
    # ---------------------------------------------------------

    if not is_solar_question(question):
        return {
            "answer": NON_SOLAR_ANSWER,
            "topic": "general",
            "sources": [],
        }

    # ---------------------------------------------------------
    # 3. Retrieve knowledge
    # ---------------------------------------------------------

    chunks = retrieve_chunks(question)

    if not chunks:
        return {
            "answer": FALLBACK_ANSWER,
            "topic": "solar",
            "sources": [],
        }

    # ---------------------------------------------------------
    # 4. Generate grounded answer
    # ---------------------------------------------------------

    answer = generate_answer(
        question,
        chunks
    ).strip()

    # ---------------------------------------------------------
    # 5. Handle insufficient knowledge
    # ---------------------------------------------------------

    if answer == FALLBACK_ANSWER:
        return {
            "answer": FALLBACK_ANSWER,
            "topic": "solar",
            "sources": [],
        }

    # ---------------------------------------------------------
    # 6. Return only sources actually supplied to the LLM
    # ---------------------------------------------------------

    sources = []

    for chunk in chunks:

        source = chunk.get("source")

        if (
            source
            and source != "unknown"
            and source not in sources
        ):
            sources.append(source)

    return {
        "answer": answer,
        "topic": "solar",
        "sources": sources,
    }