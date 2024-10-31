from fastapi import APIRouter, Request, HTTPException
from domain.models import Suggestion
from service.suggestion_service import save_suggestion


router = APIRouter()

@router.post("/send-suggestion")
async def send_suggestion(request: Request):
    try:
        form_data = await request.form()
        suggestion = Suggestion(
            nombre=form_data["nombre"],
            correo=form_data["correo"],
            mensaje=form_data["mensaje"]
        )
        save_suggestion(suggestion)
        return {"message": "Sugerencia enviada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error al procesar la solicitud")