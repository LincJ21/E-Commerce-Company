from pymongo import MongoClient
import os
from domain.cart_models import Cart

# Conectar a MongoDB
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["e_commerce"]
carts_collection = db["carts"]

def save_cart(cart: Cart):
    result = carts_collection.update_one(
        {"user_id": cart.user_id},
        {"$set": cart.dict()},
        upsert=True
    )
    return result.upserted_id

def get_cart(user_id: str) -> Cart:
    cart_data = carts_collection.find_one({"user_id": user_id})
    if cart_data:
        return Cart(**cart_data)
    return Cart(user_id=user_id)