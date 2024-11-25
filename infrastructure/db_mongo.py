from pymongo import MongoClient
import os

# Conectar a MongoDB
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["e_commerce"]
suggestions_collection = db["sugerencias"]