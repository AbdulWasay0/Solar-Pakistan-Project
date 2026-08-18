import re

from .knowledge import collection, model


TOP_K = 3


STOP_WORDS = {
    "what", "which", "how", "are", "the", "is", "in",
    "of", "for", "a", "an", "to", "and", "do", "does",
    "can", "tell", "me", "about"
}

GENERIC_WORDS = {
    "solar",
    "pakistan",
    "energy",
    "system",
    "systems"
}


def tokenize(text: str):
    return set(
        re.findall(
            r"[a-z0-9]+(?:-[a-z0-9]+)?",
            text.lower()
        )
    )


def retrieve_chunks(question: str, top_k: int = TOP_K):

    # ---------------------------------------------------------
    # 1. Embed the user's question
    # ---------------------------------------------------------

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True
    )[0]

    # ---------------------------------------------------------
    # 2. Semantic retrieval from ChromaDB
    # ---------------------------------------------------------

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=collection.count()
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    # ---------------------------------------------------------
    # 3. Find important words in the question
    # ---------------------------------------------------------

    question_words = tokenize(question)

    focus_words = (
        question_words
        - STOP_WORDS
        - GENERIC_WORDS
    )

    candidates = []

    # ---------------------------------------------------------
    # 4. Score every retrieved chunk
    # ---------------------------------------------------------

    for index, document in enumerate(documents):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )

        source = metadata.get(
            "source",
            "unknown"
        )

        # sources.md is references, not answer content
        if source == "sources.md":
            continue

        section = metadata.get(
            "section",
            "General"
        )

        distance = (
            distances[index]
            if index < len(distances)
            else 999
        )

        content_words = tokenize(document)
        section_words = tokenize(section)

        section_matches = len(
            focus_words.intersection(
                section_words
            )
        )

        content_matches = len(
            focus_words.intersection(
                content_words
            )
        )

        # Higher score = better
        #
        # Section heading matches get the strongest priority.
        # Example:
        # question = "What is a hybrid solar system?"
        # section  = "What is a hybrid system?"
        score = (
            (section_matches * 10.0)
            + (content_matches * 3.0)
            - float(distance)
        )

        candidates.append({
            "content": document,
            "source": source,
            "section": section,
            "chunk_id": metadata.get(
                "chunk_id"
            ),
            "distance": distance,
            "score": score,
            "section_matches": section_matches,
            "content_matches": content_matches
        })

    # ---------------------------------------------------------
    # 5. If question has focus words, remove unrelated chunks
    # ---------------------------------------------------------

    if focus_words:

        relevant = [
            chunk
            for chunk in candidates
            if (
                chunk["section_matches"] > 0
                or chunk["content_matches"] > 0
            )
        ]

        if relevant:
            candidates = relevant

    # ---------------------------------------------------------
    # 6. Highest score first
    # ---------------------------------------------------------

    candidates.sort(
        key=lambda chunk: chunk["score"],
        reverse=True
    )

    return candidates[:top_k]