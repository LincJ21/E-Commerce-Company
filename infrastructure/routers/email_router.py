# infrastructure/routers/email_router.py

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from use_case.email_service import send_email  # Importa el servicio de envío de correos

router = APIRouter()

@router.post("/send-email")
async def handle_send_email(request: Request):
    data = await request.json()
    name = data["name"]
    email = data["email"]
    message = data["message"]

    response = send_email(name, email, message)
    if response["message"] == "Correo enviado exitosamente":
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
