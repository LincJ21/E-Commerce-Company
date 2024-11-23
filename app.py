from fastapi import FastAPI, Request, Depends,  HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from infrastructure.db import SessionLocal
from infrastructure.routers.suggestion_router import router as suggestion_router
from interface.auth.oauth_router import router as oauth_router
from infrastructure.routers import cart_router, router_location, router_product_type, product_router
from infrastructure.repositories.product_repository import get_all_products, get_product_by_id
from domain import models, schemas
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Configurar el middleware de sesión
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "mysecret"))

app.include_router(cart_router.router)
app.include_router(router_location.router)
app.include_router(router_product_type.router)
app.include_router(product_router.router)

# Montar la carpeta de archivos estáticos (JavaScript y CSS)
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# Configurar la carpeta de plantillas
templates = Jinja2Templates(directory="templates")

# Incluir routers
app.include_router(suggestion_router)
app.include_router(oauth_router)

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

@app.get("/p", response_class=HTMLResponse)
def read_products(request: Request, db: Session = Depends(get_db)):
    products = get_all_products(db)
    return templates.TemplateResponse("P.html", {"request": request, "products": products})

@app.get("/formulario", response_class=HTMLResponse)
async def read_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})


# Iniciar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
