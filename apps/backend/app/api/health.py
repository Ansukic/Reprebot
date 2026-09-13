"""
/api/health
Estado del servicio y del conocimiento cargado.
"""

from fastapi import APIRouter

from app.core.config import get_settings
from app.services import store

router = APIRouter()


@router.get("/health")
def health():
    s = get_settings()
    return {
        "status": "ok",
        **store.store.stats(),
        "chat_model": s.groq_chat_model,
        "embeddings_model": s.embeddings_model,
    }
