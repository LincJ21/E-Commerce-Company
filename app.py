from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from infrastructure.routers.suggestion_router import router as suggestion_router
from interface.auth.oauth_router import router as oauth_router
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
load_dotenv()

import uvicorn

app = FastAPI()

# Montar la carpeta de archivos estáticos (JavaScript y CSS)
app.mount("/static", StaticFiles(directory="templates/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="contraseña al por mayor")

# Configurar la carpeta de plantillas
templates = Jinja2Templates(directory="templates")


# Incluir routers
app.include_router(suggestion_router)
app.include_router(oauth_router)


# Ruta principal para cargar el HTML en la raíz
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

# Iniciar el servidor
if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
