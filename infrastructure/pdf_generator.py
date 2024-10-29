import pdfkit

def generate_pdf(data):
    contenido_html = f"""
    <html>
        <body>
            <h1>Sugerencia o Reclamo</h1>
            <p><strong>Nombre:</strong> {data['nombre']}</p>
            <p><strong>Correo:</strong> {data['correo']}</p>
            <p><strong>Mensaje:</strong> {data['mensaje']}</p>
        </body>
    </html>
    """
    pdf_path = f"{data['nombre']}_sugerencia.pdf"
    pdfkit.from_string(contenido_html, pdf_path)
    return pdf_path
