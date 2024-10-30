from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["e_commerce"]
suggestions_collection = db["sugerencias"]

def save_suggestion(suggestion):
    result = suggestions_collection.insert_one(suggestion.dict())
    return result.inserted_id