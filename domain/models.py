from pydantic import BaseModel

class Suggestion(BaseModel):
    nombre: str
    correo: str
    mensaje: str
