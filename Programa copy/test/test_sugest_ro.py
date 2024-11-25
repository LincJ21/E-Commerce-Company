import pytest
from fastapi.testclient import TestClient
from unittest import mock
from app import app  # Asegúrate de que tu aplicación FastAPI esté importada correctamente
from service.suggestion_service import save_suggestion

client = TestClient(app)

# Mock de la función save_suggestion
def mock_save_suggestion(suggestion):
    return "mocked_id"

@pytest.fixture(autouse=True)
def setup_mocks(mocker):
    mocker.patch('service.suggestion_service.save_suggestion', side_effect=mock_save_suggestion)

def test_send_suggestion():
    form_data = {
        "nombre": "Test User",
        "correo": "test@example.com",
        "mensaje": "This is a test suggestion"
    }
    response = client.post("/send-suggestion", data=form_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Sugerencia enviada correctamente"}

def test_send_suggestion_error():
    with mock.patch('service.suggestion_service.save_suggestion', side_effect=Exception("Test Error")):
        form_data = {
            "nombre": "Test User",
            "correo": "test@example.com",
            "mensaje": "This is a test suggestion"
        }
        response = client.post("/send-suggestion", data=form_data)
        assert response.status_code == 500
        assert response.json() == {"detail": "Ocurrió un error al procesar la solicitud"}