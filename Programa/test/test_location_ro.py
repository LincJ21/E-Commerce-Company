from fastapi.testclient import TestClient
from unittest import mock
import pytest
from app import app  
from infrastructure.repositories.repository_location import get_ubicacion, create_ubicacion# Asegúrate de que tu aplicación FastAPI esté importada correctamente

client = TestClient(app)

# Simulaciones de las funciones del repositorio
def mock_get_ubicacion(db, id_ubicacion):
    if id_ubicacion == 1:
        return {"id_ubicacion": 1, "almacen": "Almacen 1", "sucursal": "Sucursal 1", "estante": "Estante 1"}
    return None

def mock_create_ubicacion(db, ubicacion):
    return {"id_ubicacion": 2, "almacen": ubicacion.almacen, "sucursal": ubicacion.sucursal, "estante": ubicacion.estante}

# Pruebas del router
@pytest.fixture
def override_get_ubicacion():
    app.dependency_overrides[get_ubicacion] = mock_get_ubicacion
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def override_create_ubicacion():
    app.dependency_overrides[create_ubicacion] = mock_create_ubicacion
    yield
    app.dependency_overrides.clear()

def test_read_ubicacion(override_get_ubicacion):
    response = client.get("/ubicacion/1")
    assert response.status_code == 200
    assert response.json() == {"id_ubicacion": 1, "almacen": "Almacen 1", "sucursal": "Sucursal 1", "estante": "Estante 1"}

def test_read_ubicacion_not_found(override_get_ubicacion):
    response = client.get("/ubicacion/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ubicación no encontrada"}

def test_create_ubicacion(override_create_ubicacion):
    response = client.post("/ubicacion/", json={"almacen": "Almacen 2", "sucursal": "Sucursal 2", "estante": "Estante 2"})
    assert response.status_code == 200
    assert response.json() == {"id_ubicacion": 2, "almacen": "Almacen 2", "sucursal": "Sucursal 2", "estante": "Estante 2"}