from app.models import chat_message


def answer(message: chat_message.ChatRequest):
    # TODO: conexión con el modelo de IA
    return chat_message.ChatResponse(body=message.body)
