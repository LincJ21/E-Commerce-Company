'''
from fpdf import FPDF
import os
from infrastructure.db_mongo import save_invoice

def generate_invoice(invoice_data: dict) -> str:
    """
    Genera una factura en formato PDF y devuelve la ruta del archivo generado.
    
    :param invoice_data: Diccionario con los detalles de la factura.
    :return: Ruta al archivo PDF generado.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt="Factura de Compra", ln=True, align="C")

    # Espaciado
    pdf.ln(10)

    # Información del cliente
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Nombre: {invoice_data['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Dirección: {invoice_data['address']}", ln=True)
    pdf.cell(200, 10, txt=f"Ciudad: {invoice_data['city']}", ln=True)
    pdf.cell(200, 10, txt=f"Código Postal: {invoice_data['postal_code']}", ln=True)

    pdf.ln(10)

    # Detalles del carrito
    pdf.cell(200, 10, txt="Detalles de la Compra:", ln=True)
    pdf.ln(5)

    for item in invoice_data['carrito']:
        pdf.cell(200, 10, txt=f"{item['nombre']} (x{item['cantidad']}) - ${item['precio']}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total: ${invoice_data['total']:.2f}", ln=True)

    # Guardar el archivo PDF
    pdf_dir = "invoices"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    file_name = f"invoice_{invoice_data['name']}.pdf"
    file_path = os.path.join(pdf_dir, file_name)
    pdf.output(file_path)

    return file_path

def process_payment_and_generate_invoice(invoice_data: dict) -> dict:
    """
    Procesa el pago y genera una factura PDF.
    
    :param invoice_data: Diccionario con los detalles del pago y la factura.
    :return: Detalles del resultado del proceso (ruta del PDF y confirmación en la base de datos).
    """
    try:
        # Generar la factura en PDF
        pdf_path = generate_invoice(invoice_data)
        
        # Guardar la factura en la base de datos (MongoDB)
        save_invoice(invoice_data)

        return {
            "message": "Factura generada y guardada correctamente.",
            "pdf_path": pdf_path
        }
    except Exception as e:
        return {
            "message": "Ocurrió un error al procesar la factura.",
            "error": str(e)
        }
'''