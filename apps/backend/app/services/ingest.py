import io

from fastapi import HTTPException
from pypdf import PdfReader

from app.core.config import get_settings
from app.services import chunker, embeddings, store

MAX_SIZE = 20 * 1024 * 1024
ALLOWED = {".pdf", ".txt", ".md"}


def _extract_text(filename: str, content: bytes) -> str:
    suffix = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if suffix == ".pdf":
        reader = PdfReader(io.BytesIO(content))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix in (".txt", ".md"):
        return content.decode("utf-8", errors="replace")
    raise HTTPException(
        415, f"formato no soportado ({suffix or 'sin extensión'}): usa pdf, txt o md"
    )


def ingest_file(filename: str, content: bytes) -> dict:
    if len(content) > MAX_SIZE:
        raise HTTPException(413, "el archivo supera 20MB")
    if len(content) == 0:
        raise HTTPException(422, "el archivo está vacío")

    text = _extract_text(filename, content)
    if not text.strip():
        raise HTTPException(
            422, "no se pudo extraer texto del archivo (¿es un pdf escaneado?)"
        )

    s = get_settings()
    chunks = chunker.chunk_text(text, s.chunk_size, s.chunk_overlap)
    if not chunks:
        raise HTTPException(422, "el documento no produjo contenido indexable")

    vectors = embeddings.embed(chunks)
    return store.store.add(filename, chunks, vectors)
