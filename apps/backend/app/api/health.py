'''
/health 
Ruta usada para realizar validaciones sobre los routers en /api/.
'''

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "Backend is up"}