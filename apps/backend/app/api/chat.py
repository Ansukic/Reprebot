"""
/chat
Ruta usada para realizar peticiones a la IA.
"""

from fastapi import APIRouter

from app.models import chat_message
from app.services.chat_service import answer

router = APIRouter()


@router.post("/chat")
def chat(message: chat_message.ChatRequest):
    return answer(message)
