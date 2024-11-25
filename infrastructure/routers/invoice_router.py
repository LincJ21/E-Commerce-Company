'''
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.cart_service2 import generate_invoice
from infrastructure.db_mongo import save_invoice

router = APIRouter()

class CartItem(BaseModel):
    id: int
    nombre: str
    precio: float
    cantidad: int

class InvoiceDetails(BaseModel):
    carrito: list[CartItem]
    total: float
    name: str
    address: str
    city: str
    postal_code: str

@router.post("/invoice")
def create_invoice(invoice_details: InvoiceDetails):
    """
    Endpoint para generar una factura.
    """
    try:
        # Generar factura PDF
        invoice_data = invoice_details.dict()
        pdf_path = generate_invoice(invoice_data)

        # Guardar factura en MongoDB
        save_invoice(invoice_data)

        return {"message": "Factura generada con éxito", "pdf_path": pdf_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''