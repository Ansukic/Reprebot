'''
/whatsapp
Ruta usada para realizar validaciones sobre el chat de whatsapp
'''


from fastapi import APIRouter

router = APIRouter()

@router.get("/whatsapp")
def whatsapp():
    return {"message": "whatsapp"}