from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from infrastructure.db import Base

# Modelos de dominio usando Pydantic
class TipoProducto(BaseModel):
    id_compra: Optional[int]
    nombre: str
    descripcion: Optional[str]

class Ubicacion(BaseModel):
    id_ubicacion: Optional[int]
    almacen: str
    sucursal: str
    estante: str

class Cliente(BaseModel):
    id_cliente: Optional[int]
    nombre: str
    email: str
    fecha_registro: Optional[str]
    id_h_compras: Optional[int]

class Direccion(BaseModel):
    id_direccion: Optional[int]
    ciudad: str
    codigo_postal: str
    barrio: str
    detalle_adicional: Optional[str]

# Modelos de base de datos usando SQLAlchemy
class TipoProductoDB(Base):
    __tablename__ = "Tipo_Producto"

    id_compra = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(Text)

class UbicacionDB(Base):
    __tablename__ = "Ubicacion"

    id_ubicacion = Column(Integer, primary_key=True, index=True)
    almacen = Column(String, index=True)
    sucursal = Column(String, index=True)
    estante = Column(String, index=True)

class ClienteDB(Base):
    __tablename__ = "Cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    fecha_registro = Column(String)
    id_h_compras = Column(Integer)

class DireccionDB(Base):
    __tablename__ = "Direccion"

    id_direccion = Column(Integer, primary_key=True, index=True)
    ciudad = Column(String, index=True)
    codigo_postal = Column(String, index=True)
    barrio = Column(String, index=True)
    detalle_adicional = Column(Text)