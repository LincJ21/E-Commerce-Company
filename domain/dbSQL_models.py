from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
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
    __tablename__ = "Tipo_Producto02"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)

class ProductoDB(Base):
    __tablename__ = "producto02"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    local_kw = Column(String, index=True)
    precio = Column(Float)
    descripcion = Column(String)
    imagen_url = Column(String)
    id_t_producto = Column(Integer, ForeignKey("Tipo_Producto02.id"))

    tipo_producto = relationship("TipoProductoDB", back_populates="productos")
    inventarios = relationship("InventarioDB", back_populates="producto")

class InventarioDB(Base):
    __tablename__ = "Inventario"

    id = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("producto02.id"))
    cantidad_disponible = Column(Integer)
    ubicacion = Column(String)

    producto = relationship("ProductoDB", back_populates="inventarios")

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
    email = Column(String, index=True)
    fecha_registro = Column(String)
    id_h_compras = Column(Integer)

TipoProductoDB.productos = relationship("ProductoDB", order_by=ProductoDB.id, back_populates="tipo_producto")
ProductoDB.inventarios = relationship("InventarioDB", order_by=InventarioDB.id, back_populates="producto")