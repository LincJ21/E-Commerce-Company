from fastapi.testclient import TestClient
from unittest import mock
import pytest
from service.email_service import send_email
from app import app  # Asegúrate de que tu aplicación FastAPI esté importada correctamente

client = TestClient(app)

# Simulaciones de las funciones del servicio de correo
def mock_send_email(name, email, message):
    if email == "success@example.com":
        return {"message": "Correo enviado exitosamente"}
    else:
        return {"message": "Error al enviar el correo"}

# Pruebas del router
@pytest.fixture
def override_send_email():
    app.dependency_overrides[send_email] = mock_send_email
    yield
    app.dependency_overrides.clear()

def test_handle_send_email_success(override_send_email):
    response = client.post("/send-email", json={"name": "John Doe", "email": "success@example.com", "message": "Hello!"})
    assert response.status_code == 200
    assert response.json() == {"message": "Correo enviado exitosamente"}

def test_handle_send_email_failure(override_send_email):
    response = client.post("/send-email", json={"name": "John Doe", "email": "failure@example.com", "message": "Hello!"})
    assert response.status_code == 500
    assert response.json() == {"message": "Error al enviar el correo"}
