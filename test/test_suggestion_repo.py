import pytest
from pymongo import MongoClient
from domain.models import Suggestion
from infrastructure.repositories.suggestion_repository import save_suggestion
import mongomock

# Configuración de la base de datos MongoDB simulada
@pytest.fixture(scope="function")
def mongo_client():
    client = mongomock.MongoClient()
    db = client["e_commerce"]
    suggestions_collection = db["sugerencias"]
    yield suggestions_collection

def test_save_suggestion(mongo_client, mocker):
    # Mockear la colección de sugerencias
    mocker.patch('suggestion_repository.suggestions_collection', mongo_client)

    # Crear un objeto Suggestion de prueba
    suggestion = Suggestion(title="Test Suggestion", description="This is a test suggestion")

    # Probar la función save_suggestion
    result_id = save_suggestion(suggestion)
    assert result_id is not None

    # Verificar que el objeto se haya guardado en la base de datos simulada
    saved_suggestion = mongo_client.find_one({"_id": result_id})
    assert saved_suggestion is not None
    assert saved_suggestion["title"] == "Test Suggestion"
    assert saved_suggestion["description"] == "This is a test suggestion"