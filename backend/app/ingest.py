from pathlib import Path

from .chroma_client import get_collection
from .embeddings import embed_texts

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"


def section_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return fallback


def chunks(text: str, max_chars: int = 12000):
    parts, buf = [], []
    for line in text.splitlines():
        if sum(len(x) for x in buf) + len(line) > max_chars and buf:
            parts.append("\n".join(buf).strip())
            buf = []
        if line.strip():
            buf.append(line)
    if buf:
        parts.append("\n".join(buf).strip())
    return parts


def main():
    collection = get_collection()
    files = sorted(DATA.glob("*.md"))
    ids, docs, metas = [], [], []

    for file in files:
        text = file.read_text(encoding="utf-8")
        title = section_title(text, file.stem.replace("_", " ").title())
        for i, chunk in enumerate(chunks(text)):
            ids.append(f"{file.stem}-{i}")
            docs.append(chunk)
            metas.append({"source": file.name, "filename": file.name, "section": title, "chunk_id": i})

    if not docs:
        raise SystemExit(f"No markdown files found in {DATA}")

    embeddings = []
    for i in range(0, len(docs), 20):
        embeddings.extend(embed_texts(docs[i:i + 20]))

    collection.upsert(ids=ids, documents=docs, embeddings=embeddings, metadatas=metas)
    print(f"Uploaded {len(docs)} chunks from {len(files)} files to Chroma Cloud.")


if __name__ == "__main__":
    main()
