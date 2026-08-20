import json
import os
import urllib.error
import urllib.parse
import urllib.request

from dotenv import load_dotenv

load_dotenv(override=True)

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
FALLBACK = (
    "I don't have enough information in the Solar Pakistan "
    "knowledge base to answer that."
)


def generate_answer(question: str, chunks: list) -> str:
    """Generate a grounded answer using only retrieved RAG chunks."""
    if not chunks:
        return FALLBACK

    context_parts = []
    for index, chunk in enumerate(chunks, start=1):
        source = chunk.get("source", "unknown")
        section = chunk.get("section", "General")
        content = chunk.get("content", "").strip()
        if content:
            context_parts.append(f"[Source {index}: {source} | {section}]\n{content}")

    if not context_parts:
        return FALLBACK

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini is not configured. Add GEMINI_API_KEY to backend/.env."

    prompt = f"""
You are Solar AI Pakistan.
Use ONLY the retrieved knowledge base below. Do not use web search, tools, or outside knowledge.
If the answer is not clearly present in the retrieved knowledge, reply exactly:
{FALLBACK}

Retrieved knowledge:
{chr(10).join(context_parts)}

Question: {question}

Answer clearly and completely using the retrieved knowledge.

Give a direct answer to the user's question first, followed by a short explanation when useful.
Do not unnecessarily shorten or truncate the answer.
Use simple language suitable for a general Pakistani solar customer.
Do not add information that is not present in the retrieved knowledge.
Include practical cautions when the knowledge says an estimate is initial only.
"""

    model = urllib.parse.quote(GEMINI_MODEL, safe="")
    key = urllib.parse.quote(api_key, safe="")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 800,
        },
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        answer = "".join(part.get("text", "") for part in parts).strip()
        return answer or FALLBACK
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini API error {error.code}: {detail}")
    except urllib.error.URLError as error:
        raise RuntimeError(f"Could not connect to Gemini: {error}")


