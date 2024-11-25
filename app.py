from fastapi import FastAPI, Request, Depends,  HTTPException, Query, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from infrastructure.db import SessionLocal
from infrastructure.routers.suggestion_router import router as suggestion_router
from interface.auth.oauth_router import router as oauth_router
from infrastructure.routers.email_router import router as email_router
from infrastructure.routers import cart_router, router_location, router_product_type, product_router
from infrastructure.repositories.product_repository import get_all_products, get_product_by_id,  create_product, update_product, delete_product, get_products_by_category
from domain import models, schemas
from dotenv import load_dotenv
#from infrastructure.routers.invoice_router import router as invoice_router
import os
import uuid
import qrcode
from PIL import Image
from fastapi import Body

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Configurar el middleware de sesión
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "mysecret"))

app.include_router(cart_router.router)
app.include_router(router_location.router)
app.include_router(router_product_type.router)
app.include_router(product_router.router)
#app.include_router(invoice_router)

# Montar la carpeta de archivos estáticos (JavaScript y CSS)
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# Configurar la carpeta de plantillas
templates = Jinja2Templates(directory="templates")

# Incluir routers
app.include_router(suggestion_router)
app.include_router(oauth_router)
app.include_router(email_router)

# Ruta principal para cargar el HTML en la raíz
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products/", response_model=schemas.Product)
def read_product(local_kw: str = Query(...), db: Session = Depends(get_db)):
    db_product = get_product_by_id(db, local_kw)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/soporte", response_class=HTMLResponse)
async def read_formulario(request: Request):
    return templates.TemplateResponse("soporte.html", {"request": request})

@app.get("/p", response_class=HTMLResponse)
def read_products(request: Request, db: Session = Depends(get_db)):
    products = get_all_products(db)
    return templates.TemplateResponse("P.html", {"request": request, "products": products, "static_images": static_images, "selected_category": selected_category})


@app.get("/product/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    static_images_path = os.path.join("templates", "static", "images")
    static_images = os.listdir(static_images_path) if os.path.exists(static_images_path) else []
    return templates.TemplateResponse("product_detail.html", {"request": request, "product": product, "static_images": static_images})

@app.get("/checkout", response_class=HTMLResponse, name="checkout")
async def checkout(request: Request):
    carrito = request.session.get("carrito", [])
    if not carrito:
        raise HTTPException(status_code=400, detail="El carrito está vacío.")
    
    total = sum(item["precio"] * item["cantidad"] for item in carrito)
    return templates.TemplateResponse(
        "checkout.html", 
        {"request": request, "carrito": carrito, "total": total}
    )


@app.get("/payment-method/{product_id}", response_class=HTMLResponse)
def payment_method(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    static_images_path = os.path.join("templates", "static", "images")
    static_images = os.listdir(static_images_path) if os.path.exists(static_images_path) else []
    return templates.TemplateResponse("payment-method.html", {"request": request, "product": product, "static_images": static_images})

@app.post("/carrito/eliminar/{product_id}")
async def eliminar_del_carrito(request: Request, product_id: int):
    carrito = request.session.get("carrito", [])
    carrito = [item for item in carrito if item["id"] != product_id]  # Filtrar el producto a eliminar
    request.session["carrito"] = carrito  # Actualizar el carrito en la sesión
    return RedirectResponse(url="/carrito", status_code=303)


@app.post("/process-payment/{product_id}", response_class=HTMLResponse)
def process_payment(product_id: int, payment_method: str = Form(...), db: Session = Depends(get_db)):
    # Lógica para procesar el pago
    return {"message": "Pago procesado"}


@app.get("/invoice", response_class=HTMLResponse, name="invoice")
def get_invoice(
    request: Request,
    carrito: list = Query([]),
    total: float = Query(0.0),
    name: str = Query(""),
    address: str = Query(""),
    city: str = Query(""),
    postal_code: str = Query("")
):
    # Convertir el carrito en una estructura procesable
    carrito_procesado = []
    for item in carrito:
        carrito_procesado.append({
            "id": item.get("id"),
            "nombre": item.get("nombre"),
            "precio": float(item.get("precio", 0)),
            "cantidad": int(item.get("cantidad", 1))
        })

    # Generar un código numeral único
    payment_code = str(uuid.uuid4().int)[:10]  # Un número único de 10 dígitos

    # Generar el código QR basado en el código numeral
    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4
    )
    qr.add_data(payment_code)
    qr.make(fit=True)
    qr_img = qr.make_image(fill="black", back_color="white")
    qr_code_filename = f"qr_{payment_code}.png"
    qr_code_path = os.path.join("templates", "static", "images", qr_code_filename)
    qr_img.save(qr_code_path)

    payment_details = {
        "carrito": carrito_procesado,
        "total": total,
        "name": name,
        "address": address,
        "city": city,
        "postal_code": postal_code,
        "payment_code": payment_code,
        "qr_code_filename": qr_code_filename
    }

    return templates.TemplateResponse("invoice.html", {"request": request, "payment_details": payment_details})




@app.post("/products/", response_model=schemas.Product)
def create_new_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_existing_product(product_id: int, updated_product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return update_product(db, product_id, updated_product)

@app.delete("/products/{product_id}")
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    delete_product(db, product_id)
    return {"message": "Producto eliminado"}

@app.get("/formulario", response_class=HTMLResponse)
async def read_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.get("/carrito", response_class=HTMLResponse)
async def carrito_compra(request: Request):
    carrito = request.session.get("carrito", [])
    total = sum(item["precio"] * item["cantidad"] for item in carrito)
    return templates.TemplateResponse("carrito_compra.html", {"request": request, "carrito": carrito, "total": total})

@app.post("/carrito/agregar/{product_id}", response_class=RedirectResponse)
async def agregar_al_carrito(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    carrito = request.session.get("carrito", [])
    for item in carrito:
        if item["id"] == product_id:
            item["cantidad"] += 1
            break
    else:
        carrito.append({"id": product.id, "nombre": product.nombre, "precio": product.precio, "cantidad": 1})
    
    request.session["carrito"] = carrito
    return RedirectResponse(url="/carrito", status_code=303)

# Iniciar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
