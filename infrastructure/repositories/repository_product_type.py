from sqlalchemy.orm import Session
from domain.dbSQL_models import TipoProductoDB, TipoProducto

def get_tipo_producto(db: Session, id_compra: int):
    return db.query(TipoProductoDB).filter(TipoProductoDB.id_compra == id_compra).first()

def create_tipo_producto(db: Session, tipo_producto: TipoProducto):
    db_tipo_producto = TipoProductoDB(**tipo_producto.dict())
    db.add(db_tipo_producto)
    db.commit()
    db.refresh(db_tipo_producto)
    return db_tipo_producto