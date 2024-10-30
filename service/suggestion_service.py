from infrastructure.db import suggestions_collection
from infrastructure.pdf_generator import generate_pdf
from domain.models import Suggestion

def save_suggestion(data: Suggestion):
    # Convertir el modelo Pydantic en un diccionario y guardarlo en MongoDB
    suggestion_data = data.dict()
    suggestions_collection.insert_one(suggestion_data)

    # Generar PDF
    pdf_path = generate_pdf(suggestion_data)
    return pdf_path
