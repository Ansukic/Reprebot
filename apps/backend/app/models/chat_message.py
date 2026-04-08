from pydantic import BaseModel

class ChatRequest(BaseModel):
    body: str


class ChatResponse(BaseModel):
    body: str