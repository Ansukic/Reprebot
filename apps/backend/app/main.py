from fastapi import Depends, FastAPI

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.whatsapp import router as whatsapp_router

app = FastAPI()
app.include_router(whatsapp_router)
app.include_router(health_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Hello world!"}

