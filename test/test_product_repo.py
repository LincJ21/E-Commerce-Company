import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from domain.product_models import Product
from infrastructure.repositories.product_repository import (
    get_product,
    search_products,
    create_product,
    update_product,
    delete_product,
    ProductDB
)

@pytest.fixture
def mock_db_session():
    """Crea un mock de la sesión de la base de datos."""
    return MagicMock(spec=Session)

@pytest.fixture
def sample_product():
    """Devuelve un producto de ejemplo."""
    return Product(id="prod1", name="Sample Product", price=100.0, description="A sample product description")

@pytest.fixture
def sample_product_db():
    """Devuelve un producto de ejemplo en formato DB."""
    return ProductDB(id="prod1", name="Sample Product", price=100.0, description="A sample product description")

# Prueba para `get_product`
def test_get_product(mock_db_session, sample_product_db):
    """Prueba que obtiene un producto de la base de datos."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = sample_product_db
    
    product = get_product(mock_db_session, "prod1")
    
    assert product.id == "prod1"
    assert product.name == "Sample Product"

# Prueba para `search_products`
def test_search_products(mock_db_session, sample_product_db):
    """Prueba que busca productos en la base de datos."""
    mock_db_session.query.return_value.filter.return_value.ilike.return_value.all.return_value = [sample_product_db]
    
    products = search_products(mock_db_session, "Sample")
    
    assert len(products) == 1
    assert products[0].id == sample_product_db.id
    assert products[0].name == sample_product_db.name

# Prueba para `create_product`
def test_create_product(mock_db_session, sample_product):
    """Prueba que crea un nuevo producto en la base de datos."""
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()
    
    created_product = create_product(mock_db_session, sample_product)
    
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    assert created_product.name == "Sample Product"

# Prueba para `update_product`
def test_update_product(mock_db_session, sample_product_db, sample_product):
    """Prueba que actualiza un producto existente en la base de datos."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = sample_product_db
    
    updated_product = update_product(mock_db_session, "prod1", sample_product)
    
    assert updated_product.name == "Sample Product"
    mock_db_session.commit.assert_called_once()

# Prueba para `delete_product`
def test_delete_product(mock_db_session, sample_product_db):
    """Prueba que elimina un producto de la base de datos."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = sample_product_db
    
    deleted_product = delete_product(mock_db_session, "prod1")
    
    assert deleted_product.id == "prod1"
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()