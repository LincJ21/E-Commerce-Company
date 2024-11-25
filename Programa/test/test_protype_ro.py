import pytest
from fastapi.testclient import TestClient
from unittest import mock
from app import app  # Asegúrate de que tu aplicación FastAPI esté importada correctamente
from domain.dbSQL_models import TipoProducto
from infrastructure.repositories.repository_product_type import get_tipo_producto, create_tipo_producto

client = TestClient(app)

# Mock de la función get_tipo_producto
def mock_get_tipo_producto(db, id_compra):
    if id_compra == 1:
        return TipoProducto(id_compra=1, nombre="Producto de prueba")
    return None

# Mock de la función create_tipo_producto
def mock_create_tipo_producto(db, tipo_producto):
    return TipoProducto(id_compra=tipo_producto.id_compra, nombre=tipo_producto.nombre)

@pytest.fixture(autouse=True)
def setup_mocks(mocker):
    mocker.patch('infrastructure.repositories.repository_product_type.get_tipo_producto', side_effect=mock_get_tipo_producto)
    mocker.patch('infrastructure.repositories.repository_product_type.create_tipo_producto', side_effect=mock_create_tipo_producto)

def test_read_tipo_producto():
    response = client.get("/tipo_producto/1")
    assert response.status_code == 200
    assert response.json() == {"id_compra": 1, "nombre": "Producto de prueba"}

    response = client.get("/tipo_producto/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Tipo de producto no encontrado"}

def test_create_tipo_producto():
    new_tipo_producto = {"id_compra": 2, "nombre": "Nuevo Producto"}
    response = client.post("/tipo_producto/", json=new_tipo_producto)
    assert response.status_code == 200
    assert response.json() == new_tipo_producto