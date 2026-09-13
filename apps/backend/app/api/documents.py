"""
/api/documents
Ingesta, listado y borrado de documentos del conocimiento.
"""

from fastapi import APIRouter, Header, HTTPException, UploadFile

from app.core.config import get_settings
from app.models.chat_message import DocumentInfo, DocumentListResponse
from app.services import ingest, store

router = APIRouter()


def _check_admin(x_admin_token: str | None):
    token = get_settings().admin_token
    if token and x_admin_token != token:
        raise HTTPException(401, "token de administrador inválido")


@router.post("/documents", response_model=DocumentInfo)
async def upload_document(file: UploadFile, x_admin_token: str | None = Header(None)):
    _check_admin(x_admin_token)
    content = await file.read()
    return ingest.ingest_file(file.filename or "documento", content)


@router.get("/documents", response_model=DocumentListResponse)
def list_documents():
    return {"documents": store.store.list_docs()}


@router.delete("/documents/{doc_id}", status_code=204)
def delete_document(doc_id: str, x_admin_token: str | None = Header(None)):
    _check_admin(x_admin_token)
    if not store.store.remove_doc(doc_id):
        raise HTTPException(404, "documento no encontrado")
