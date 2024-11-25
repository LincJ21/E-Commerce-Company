from pymongo import MongoClient
import os
from domain.models import Suggestion

# Conectar a MongoDB
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["e_commerce"]
suggestions_collection = db["sugerencias"]

def save_suggestion(suggestion: Suggestion):
    result = suggestions_collection.insert_one(suggestion.dict())
    return result.inserted_id