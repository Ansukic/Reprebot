"""
/api/chat
Pregunta al RAG: recupera contexto y genera respuesta con fuentes.
"""

from fastapi import APIRouter

from app.models.chat_message import ChatRequest, ChatResponse
from app.services import rag

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return rag.answer_question(req.question, req.k)
