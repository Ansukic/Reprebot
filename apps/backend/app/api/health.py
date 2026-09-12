"""
/health
Ruta usada para verificar que el backend está arriba.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "Backend is up"}
