from pymongo import MongoClient
import os

# Conectar a MongoDB
try:
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    client.admin.command('ping')  # Verifica conexión con MongoDB
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    raise e

# Selección de la base de datos
db = client["e_commerce"]

# Colecciones
suggestions_collection = db["sugerencias"]
invoices_collection = db["invoices"]

# Función para guardar sugerencias
def save_suggestion(suggestion_details):
    """
    Guarda una sugerencia en la colección 'sugerencias'.
    :param suggestion_details: Diccionario con los detalles de la sugerencia.
    """
    try:
        result = suggestions_collection.insert_one(suggestion_details)
        print(f"Sugerencia guardada con ID: {result.inserted_id}")
        return {"status": "success", "id": str(result.inserted_id)}
    except Exception as e:
        print(f"Error al guardar sugerencia: {e}")
        return {"status": "error", "message": str(e)}

# Función para guardar facturas
def save_invoice(payment_details):
    """
    Guarda los detalles de una factura en la colección 'invoices'.
    :param payment_details: Diccionario con los detalles del pago.
    """
    try:
        result = invoices_collection.insert_one(payment_details)
        print(f"Factura guardada con ID: {result.inserted_id}")
        return {"status": "success", "id": str(result.inserted_id)}
    except Exception as e:
        print(f"Error al guardar factura: {e}")
        return {"status": "error", "message": str(e)}
