from sqlalchemy.orm import Session
from domain.product_models import Product
from infrastructure.db import Base
from sqlalchemy import Column, String, Float
from typing import List

class ProductDB(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)

def get_product(db: Session, product_id: str) -> ProductDB:
    return db.query(ProductDB).filter(ProductDB.id == product_id).first()

def search_products(db: Session, name: str) -> list[ProductDB]:
    return db.query(ProductDB).filter(ProductDB.name.ilike(f"%{name}%")).all()

def create_product(db: Session, product: Product) -> ProductDB:
    db_product = ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: str, updated_product: Product) -> ProductDB:
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if product:
        for key, value in updated_product.dict().items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product

def delete_product(db: Session, product_id: str):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product