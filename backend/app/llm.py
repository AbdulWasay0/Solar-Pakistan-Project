import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"
FALLBACK = (
    "I don't have enough information in the Solar Pakistan "
    "knowledge base to answer that."
)


def generate_answer(question: str, chunks: list) -> str:
    """
    Generate a grounded answer using Ollama and
    knowledge retrieved from ChromaDB.
    """

    if not chunks:
        return FALLBACK

    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        source = chunk.get("source", "unknown")
        content = chunk.get("content", "")

        if content.strip():
            context_parts.append(f"[Source {index}: {source}]\n{content}")

    if not context_parts:
        return FALLBACK

    context = "\n\n".join(context_parts)

    prompt = f"""
You are Solar AI Pakistan.

Answer the user's question using the RETRIEVED KNOWLEDGE below.

RETRIEVED KNOWLEDGE:
--------------------
{context}
--------------------

USER QUESTION:
{question}

RULES:
1. Use the retrieved knowledge as your source.
2. If relevant information is present, answer clearly and directly.
3. You may combine relevant information from multiple retrieved passages.
4. Ignore passages that are unrelated to the question.
5. Do not invent prices, specifications, regulations, warranties,
   or technical facts that are not supported by the retrieved knowledge.
6. Keep the answer concise.
7. If the retrieved knowledge contains no relevant information at all,
   respond exactly:
"{FALLBACK}"

ANSWER:
"""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0, "num_predict": 180},
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            answer = result.get("response", "").strip()

        fallback_variants = [
            FALLBACK,
            "I do not have enough information in the Solar Pakistan knowledge base to answer that.",
        ]

        for fallback in fallback_variants:
            if fallback in answer and answer.strip() != fallback:
                answer = answer.replace(fallback, "").strip()

        prefixes = [
            "I am Solar AI Pakistan.",
            "I am Solar AI Pakistan.\n",
            "Based on the retrieved knowledge,",
        ]

        for prefix in prefixes:
            if answer.startswith(prefix):
                answer = answer[len(prefix):].strip()

        return answer or FALLBACK
    except urllib.error.URLError as error:
        raise RuntimeError(f"Could not connect to Ollama: {error}")
