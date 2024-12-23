from domain.cart_models import Cart, CartItem, Product
from infrastructure.repositories.cart_repository import save_cart, get_cart
from infrastructure.repositories.product_repository import get_all_products
from sqlalchemy.orm import Session

def add_product_to_cart(db: Session, user_id: str, product_id: int, quantity: int):
    product = get_all_products(db, product_id)
    if not product:
        raise ValueError("Producto no encontrado")

    cart = get_cart(user_id)
    for item in cart.items:
        if item.product.id == product.id:
            item.quantity += quantity
            break
    else:
        cart.items.append(CartItem(product=product, quantity=quantity))
    save_cart(cart)

def remove_product_from_cart(user_id: str, product_id: int):
    cart = get_cart(user_id)
    cart.items = [item for item in cart.items if item.product.id != product_id]
    save_cart(cart)

def get_user_cart(user_id: str) -> Cart:
    return get_cart(user_id)