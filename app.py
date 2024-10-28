from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from infrastructure.routers import email_router  # Importar otros routers según sea necesario
from dotenv import load_dotenv
load_dotenv()

import uvicorn

app = FastAPI()

# Montar la carpeta de archivos estáticos (JavaScript y CSS)
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# Configurar la carpeta de plantillas
templates = Jinja2Templates(directory="templates")

# Incluir los routers
app.include_router(email_router.router)

# Ruta principal para cargar el HTML en la raíz
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

# Iniciar el servidor
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
