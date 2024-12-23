from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infrastructure.db import SessionLocal
from domain.product_models import Product
from infrastructure.repositories.product_repository import get_all_products, create_product, update_product, delete_product

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_all_products(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/products/", response_model=Product)
async def create_new_product(product: Product, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.put("/products/{product_id}", response_model=Product)
async def update_existing_product(product_id: int, updated_product: Product, db: Session = Depends(get_db)):
    product = update_product(db, product_id, updated_product)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.delete("/products/{product_id}")
async def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    delete_product(db, product_id)
    return {"message": "Producto eliminado"}