from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infrastructure.db import SessionLocal
from service.cart_service import add_product_to_cart, remove_product_from_cart, get_user_cart

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cart/{user_id}/add")
async def add_to_cart(user_id: str, product_id: str, quantity: int, db: Session = Depends(get_db)):
    try:
        add_product_to_cart(db, user_id, product_id, quantity)
        return {"message": "Producto añadido al carrito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error al añadir el producto al carrito")

@router.post("/cart/{user_id}/remove")
async def remove_from_cart(user_id: str, product_id: str):
    try:
        remove_product_from_cart(user_id, product_id)
        return {"message": "Producto eliminado del carrito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error al eliminar el producto del carrito")

@router.get("/cart/{user_id}")
async def get_cart(user_id: str):
    try:
        cart = get_user_cart(user_id)
        return cart
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error al obtener el carrito")