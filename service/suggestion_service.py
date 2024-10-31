from infrastructure.db_mongo import suggestions_collection
from domain.models import Suggestion

def save_suggestion(data: Suggestion):
    # Convertir el modelo Pydantic en un diccionario y guardarlo en MongoDB
    suggestion_data = data.dict()
    suggestions_collection.insert_one(suggestion_data)
    return suggestion_data