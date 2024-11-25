import pytest
from unittest.mock import MagicMock, patch
from domain.cart_models import Cart, CartItem, Product
from infrastructure.repositories.cart_repository import save_cart, get_cart

@pytest.fixture
def sample_product():
    """Devuelve un producto de ejemplo."""
    return Product(id="prod1", name="Sample Product", price=100, description="A sample product description")

@pytest.fixture
def sample_cart(sample_product):
    """Devuelve un carrito de ejemplo."""
    item = CartItem(product=sample_product, quantity=2)  # Usa el producto de ejemplo
    return Cart(user_id="user1", items=[item])

# Pruebas para `save_cart`
def test_save_cart(sample_cart):
    """Prueba que guarda un carrito en la base de datos."""
    with patch("infrastructure.repositories.cart_repository.carts_collection") as mock_collection:
        mock_collection.update_one.return_value = MagicMock(upserted_id="some_id")
        
        result = save_cart(sample_cart)
        
        # Verifica que se llamó a update_one con los parámetros correctos
        mock_collection.update_one.assert_called_once_with(
            {"user_id": sample_cart.user_id},
            {"$set": sample_cart.dict()},
            upsert=True
        )
        assert result == "some_id"  # Verifica que el ID devuelto sea el esperado

# Pruebas para `get_cart`
def test_get_cart_existing_cart(sample_cart):
    """Prueba que obtiene un carrito existente de la base de datos."""
    with patch("infrastructure.repositories.cart_repository.carts_collection") as mock_collection:
        mock_collection.find_one.return_value = sample_cart.dict()  # Simula que se encuentra el carrito
        
        result = get_cart("user1")
        
        # Verifica que el carrito devuelto sea el correcto
        assert result.user_id == sample_cart.user_id
        assert len(result.items) == 1
        assert result.items[0].quantity == 2

def test_get_cart_non_existing_cart():
    """Prueba que devuelve un carrito vacío si no existe."""
    with patch("infrastructure.repositories.cart_repository.carts_collection") as mock_collection:
        mock_collection.find_one.return_value = None  # Simula que no se encuentra el carrito
        
        result = get_cart("user2")
        
        # Verifica que se devuelva un carrito vacío
        assert result.user_id == "user2"
        assert len(result.items) == 0


