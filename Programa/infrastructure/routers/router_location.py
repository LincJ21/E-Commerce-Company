from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infrastructure.db import SessionLocal
from domain.dbSQL_models import Ubicacion
from infrastructure.repositories.repository_location import get_ubicacion, create_ubicacion

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ubicacion/{id_ubicacion}")
async def read_ubicacion(id_ubicacion: int, db: Session = Depends(get_db)):
    ubicacion = get_ubicacion(db, id_ubicacion)
    if ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return ubicacion

@router.post("/ubicacion/")
async def create_ubicacion(ubicacion: Ubicacion, db: Session = Depends(get_db)):
    return create_ubicacion(db, ubicacion)