from sqlalchemy.orm import Session
from domain.dbSQL_models import Ubicacion, UbicacionDB

def get_ubicacion(db: Session, id_ubicacion: int):
    return db.query(UbicacionDB).filter(UbicacionDB.id_ubicacion == id_ubicacion).first()

def create_ubicacion(db: Session, ubicacion: Ubicacion):
    db_ubicacion = UbicacionDB(**ubicacion.dict())
    db.add(db_ubicacion)
    db.commit()
    db.refresh(db_ubicacion)
    return db_ubicacion