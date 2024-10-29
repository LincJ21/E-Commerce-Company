from fastapi import APIRouter, Request, HTTPException
from domain.models import Suggestion
from infrastructure.db import suggestions_collection  # Asegúrate de importar la colección correcta

router = APIRouter()

@router.post("/send-suggestion")
async def send_suggestion(request: Request):
    try:
        print("Inicio del endpoint /send-suggestion")  # Verifica que el endpoint fue llamado
        form_data = await request.form()
        print("Datos del formulario recibidos:", form_data)  # Verifica si los datos del formulario fueron recibidos correctamente
        suggestion = Suggestion(
            nombre=form_data["nombre"],
            correo=form_data["correo"],
            mensaje=form_data["mensaje"]
        )
        # Guardar la sugerencia en MongoDB
        result = suggestions_collection.insert_one(suggestion.dict())
        print(f"Sugerencia insertada con ID: {result.inserted_id}")
        return {"message": "Sugerencia enviada correctamente"}
    except Exception as e:
        print("Error en el endpoint /send-suggestion:", e)  # Imprime el error para ver más detalles
        raise HTTPException(status_code=500, detail="Ocurrió un error al procesar la solicitud")