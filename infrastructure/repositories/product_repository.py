from sqlalchemy.orm import Session
from domain.dbSQL_models import ProductoDB
from domain import schemas

def get_product_by_id(db: Session, product_id: int):
    return db.query(ProductoDB).filter(ProductoDB.id == product_id).first()

def get_all_products(db: Session):
    return db.query(ProductoDB).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = ProductoDB(
        nombre=product.nombre,
        local_kw=product.local_kw,
        id_t_producto=product.id_t_producto,
        imagen_url=product.imagen_url,
        precio=product.precio,
        descripcion=product.descripcion
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, updated_product: schemas.ProductUpdate):
    product = db.query(ProductoDB).filter(ProductoDB.id == product_id).first()
    if product:
        for key, value in updated_product.dict().items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(ProductoDB).filter(ProductoDB.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product