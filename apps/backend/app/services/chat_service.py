
from ..models import chat_message


def answer(message: chat_message.ChatRequest):
    #Aquí iría la conexión con request a la IA

    return chat_message.ChatResponse(body=message.body)