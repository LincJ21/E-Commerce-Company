from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from infrastructure.routers.suggestion_router import router as suggestion_router
from infrastructure.routers import cart_router, router_location, router_product_type, product_router
from dotenv import load_dotenv
load_dotenv()

import uvicorn
app = FastAPI()


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

# Ruta principal para cargar el HTML en la raíz
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/formulario", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.get("/carrito", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("carrito_compra.html", {"request": request})

# Iniciar el servidor
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
