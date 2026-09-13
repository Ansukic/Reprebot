from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.api.search import router as search_router
from app.core.config import get_settings
from app.services import store


@asynccontextmanager
async def lifespan(app: FastAPI):
    store.store.load()
    yield


settings = get_settings()

app = FastAPI(title="Reprebot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(documents_router, prefix="/api")

frontend = Path(__file__).resolve().parent.parent.parent / "frontend"
if frontend.is_dir():
    # va al final: /api/* y /docs ganan sobre los estáticos
    app.mount("/", StaticFiles(directory=frontend, html=True), name="ui")
else:

    @app.get("/")
    def root():
        return {"name": "reprebot", "docs": "/docs"}
