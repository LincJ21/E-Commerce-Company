from unittest import mock
import pytest

# Supongamos que tu modelo UbicacionDB está definido aquí
class UbicacionDB:
    def __init__(self, almacen, sucursal, estante):
        self.almacen = almacen
        self.sucursal = sucursal
        self.estante = estante

# Función que quieres probar
def crear_ubicacion(session, almacen, sucursal, estante):
    if not almacen:
        raise ValueError("El almacen no puede ser None")
    nueva_ubicacion = UbicacionDB(almacen, sucursal, estante)
    session.add(nueva_ubicacion)
    return nueva_ubicacion

# Pruebas
def test_crear_ubicacion():
    mock_session = mock.Mock()
    ubicacion = crear_ubicacion(mock_session, "Almacen 1", "Sucursal 1", "Estante 1")
    assert ubicacion.almacen == "Almacen 1"
    mock_session.add.assert_called_once_with(ubicacion)

def test_crear_ubicacion_error():
    mock_session = mock.Mock()
    with pytest.raises(ValueError):
        crear_ubicacion(mock_session, None, "Sucursal 2", "Estante 2")
