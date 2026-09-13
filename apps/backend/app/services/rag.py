from app.services import ai_client, embeddings, store

SYSTEM_PROMPT = """Eres Reprebot, asistente del Consejo de Estudiantes de Ingeniería de Sistemas (CEIS) de la Universidad Nacional de Colombia. Respondes preguntas sobre la UNAL usando únicamente el contexto proporcionado.

Reglas:
- Responde SOLO con información presente en el contexto. No inventes normas, artículos ni fechas.
- Cita de qué documento proviene la información, por ejemplo: (Reglamento General de Estudiantes).
- Si el contexto no alcanza para responder, dilo claramente y sugiere consultar la fuente oficial.
- Máximo 3 párrafos, en español, directo al punto."""


def answer_question(question: str, k: int) -> dict:
    if not store.store.chunks:
        return {
            "answer": "Aún no tengo conocimiento cargado. Sube documentos primero desde la pestaña de documentos.",
            "sources": [],
        }

    query_vec = embeddings.embed([question])[0]
    results = store.store.search(query_vec, k)

    context = "\n\n".join(
        f"[{i}] ({r['doc_name']})\n{r['text']}" for i, r in enumerate(results, 1)
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Contexto:\n\n{context}\n\nPregunta: {question}"},
    ]
    answer = ai_client.chat(messages)

    sources = [
        {
            "doc_id": r["doc_id"],
            "doc_name": r["doc_name"],
            "text": r["text"],
            "score": r["score"],
        }
        for r in results
    ]
    return {"answer": answer, "sources": sources}


def search(question: str, k: int) -> list[dict]:
    if not store.store.chunks:
        return []
    query_vec = embeddings.embed([question])[0]
    return [
        {
            "doc_id": r["doc_id"],
            "doc_name": r["doc_name"],
            "text": r["text"],
            "score": r["score"],
        }
        for r in store.store.search(query_vec, k)
    ]
