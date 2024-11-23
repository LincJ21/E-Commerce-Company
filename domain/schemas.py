from pydantic import BaseModel

class ProductBase(BaseModel):
    nombre: str
    local_kw: str
    imagen_url: str
    precio: float
    descripcion: str

class ProductCreate(ProductBase):
    id_t_producto: int

class ProductUpdate(ProductBase):
    id_t_producto: int

class Product(ProductBase):
    id: int
    id_t_producto: int

    class Config:
        from_attributes = True