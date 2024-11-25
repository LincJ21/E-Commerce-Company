import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.dbSQL_models import Base, TipoProductoDB, TipoProducto
from infrastructure.repositories.repository_product_type import get_tipo_producto, create_tipo_producto

# Configuración de la base de datos en memoria para pruebas
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos en memoria
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Crea una nueva sesión de base de datos para cada prueba."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_get_tipo_producto(db_session):
    # Crear un objeto TipoProductoDB de prueba
    tipo_producto = TipoProductoDB(id_compra=1, nombre="Producto de prueba")
    db_session.add(tipo_producto)
    db_session.commit()

    # Probar la función get_tipo_producto
    result = get_tipo_producto(db_session, 1)
    assert result is not None
    assert result.id_compra == 1
    assert result.nombre == "Producto de prueba"

def test_create_tipo_producto(db_session):
    # Crear un objeto TipoProducto de prueba
    tipo_producto = TipoProducto(id_compra=2, nombre="Nuevo Producto")

    # Probar la función create_tipo_producto
    result = create_tipo_producto(db_session, tipo_producto)
    assert result is not None
    assert result.id_compra == 2
    assert result.nombre == "Nuevo Producto"

    # Verificar que el objeto se haya guardado en la base de datos
    db_result = db_session.query(TipoProductoDB).filter(TipoProductoDB.id_compra == 2).first()
    assert db_result is not None
    assert db_result.id_compra == 2
    assert db_result.nombre == "Nuevo Producto"