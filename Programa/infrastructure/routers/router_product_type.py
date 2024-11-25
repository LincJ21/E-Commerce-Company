from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infrastructure.db import SessionLocal
from domain.dbSQL_models import TipoProducto
from infrastructure.repositories.repository_product_type import get_tipo_producto, create_tipo_producto

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tipo_producto/{id_compra}")
async def read_tipo_producto(id_compra: int, db: Session = Depends(get_db)):
    tipo_producto = get_tipo_producto(db, id_compra)
    if tipo_producto is None:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    return tipo_producto

@router.post("/tipo_producto/")
async def create_tipo_producto(tipo_producto: TipoProducto, db: Session = Depends(get_db)):
    return create_tipo_producto(db, tipo_producto)