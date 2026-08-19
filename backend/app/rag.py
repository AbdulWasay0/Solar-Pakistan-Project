import re

from .chroma_client import get_collection
from .embeddings import embed_texts

TOP_K = 3
STOP_WORDS = {"what", "which", "how", "are", "the", "is", "in", "of", "for", "a", "an", "to", "and", "do", "does", "can", "tell", "me", "about"}
GENERIC_WORDS = {"solar", "pakistan", "energy", "system", "systems"}


def tokenize(text: str):
    return set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", text.lower()))


def retrieve_chunks(question: str, top_k: int = TOP_K):
    query_embedding = embed_texts([question])[0]
    results = get_collection().query(query_embeddings=[query_embedding], n_results=top_k * 2)
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    focus_words = tokenize(question) - STOP_WORDS - GENERIC_WORDS
    chunks = []

    for i, document in enumerate(documents):
        metadata = metadatas[i] if i < len(metadatas) else {}
        source = metadata.get("source") or metadata.get("filename") or "unknown"
        if source == "sources.md":
            continue
        section = metadata.get("section", "General")
        if focus_words and not focus_words.intersection(tokenize(document + " " + section)):
            continue
        chunks.append({
            "content": document,
            "source": source,
            "section": section,
            "chunk_id": metadata.get("chunk_id"),
            "distance": distances[i] if i < len(distances) else None,
        })

    return chunks[:top_k]
