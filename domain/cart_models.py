from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    id: str
    name: str
    price: float
    description: str

class CartItem(BaseModel):
    product: Product
    quantity: int

class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []