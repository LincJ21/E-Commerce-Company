from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infrastructure.db import SessionLocal
from domain.product_models import Product
from typing import List
from infrastructure.repositories.product_repository import get_product, create_product, update_product, delete_product, search_products

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: str, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.get("/products/", response_model=List[Product])
async def search_products(name: str, db: Session = Depends(get_db)):
    if name is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return search_products(db, name=name)

@router.post("/products/", response_model=Product)
async def create_new_product(product: Product, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.put("/products/{product_id}", response_model=Product)
async def update_existing_product(product_id: str, updated_product: Product, db: Session = Depends(get_db)):
    product = update_product(db, product_id, updated_product)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.delete("/products/{product_id}")
async def delete_existing_product(product_id: str, db: Session = Depends(get_db)):
    delete_product(db, product_id)
    return {"message": "Producto eliminado"}