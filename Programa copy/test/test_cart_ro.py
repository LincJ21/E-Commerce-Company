import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app  # Asegúrate de que 'app' es tu archivo principal

client = TestClient(app)

# Prueba para añadir un producto al carrito
def test_add_to_cart():
    with patch("service.cart_service.add_product_to_cart") as mock_add:
        mock_add.return_value = None  # Simula que la función se ejecuta sin errores
        
        response = client.post("/cart/user1/add", json={"product_id": "prod1", "quantity": 2})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Producto añadido al carrito"}
        mock_add.assert_called_once_with(MagicMock(), "user1", "prod1", 2)

# Prueba para eliminar un producto del carrito
def test_remove_from_cart():
    with patch("service.cart_service.remove_product_from_cart") as mock_remove:
        mock_remove.return_value = None  # Simula que la función se ejecuta sin errores
        
        response = client.post("/cart/user1/remove", json={"product_id": "prod1"})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Producto eliminado del carrito"}
        mock_remove.assert_called_once_with("user1", "prod1")

# Prueba para obtener el carrito
def test_get_cart():
    with patch("service.cart_service.get_user_cart") as mock_get:
        mock_get.return_value = {"user_id": "user1", "items": []}  # Simula un carrito vacío
        
        response = client.get("/cart/user1")
        
        assert response.status_code == 200
        assert response.json() == {"user_id": "user1", "items": []}
        mock_get.assert_called_once_with("user1")

# Prueba para manejar errores al añadir un producto
def test_add_to_cart_error():
    with patch("service.cart_service.add_product_to_cart") as mock_add:
        mock_add.side_effect = Exception("Error al añadir producto")  # Simula un error
        
        response = client.post("/cart/user1/add", json={"product_id": "prod1", "quantity": 2})
        
        assert response.status_code == 500
        assert response.json() == {"detail": "Ocurrió un error al añadir el producto al carrito"}

# Prueba para manejar errores al eliminar un producto
def test_remove_from_cart_error():
    with patch("service.cart_service.remove_product_from_cart") as mock_remove:
        mock_remove.side_effect = Exception("Error al eliminar producto")  # Simula un error
    
        response = client.post("/cart/user1/remove", json={"product_id": "prod1"})
        
        assert response.status_code == 500
        assert response.json() == {"detail": "Ocurrió un error al eliminar el producto del carrito"}

# Prueba para manejar errores al obtener el carrito
def test_get_cart_error():
    with patch("service.cart_service.get_user_cart") as mock_get:
        mock_get.side_effect = Exception("Error al obtener carrito")  # Simula un error
        
        response = client.get("/cart/user1")
        
        assert response.status_code == 500
        assert response.json() == {"detail": "Ocurrió un error al obtener el carrito"}
