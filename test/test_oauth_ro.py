from fastapi.testclient import TestClient
from unittest import mock
import pytest
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

# Configuración de la aplicación FastAPI
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
client = TestClient(app)

# Simulación de la configuración de OAuth
oauth = mock.Mock()
oauth.google.authorize_redirect = mock.AsyncMock(return_value=RedirectResponse(url="/auth"))
oauth.google.authorize_access_token = mock.AsyncMock(return_value={"userinfo": {"name": "John Doe", "email": "john.doe@example.com"}})

# Definición de las rutas
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/login")
async def login():
    return RedirectResponse(url="/auth")

@app.get("/auth")
async def auth():
    return {"message": "Authenticated"}

@app.get("/inicio")
async def inicio():
    return {"message": "Welcome"}

@app.get("/logout")
async def logout():
    return {"message": "Logged out"}

# Funciones de prueba
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_login_redirect():
    response = client.get("/login")
    assert response.status_code == 200

def test_auth_success():
    response = client.get("/auth")
    assert response.status_code == 200

def test_welcome_authenticated():
    with client:
        client.cookies.set("session", "test_session")
        response = client.get("/inicio")
        assert response.status_code == 200

def test_welcome_unauthenticated():
    response = client.get("/inicio")
    assert response.status_code == 401

def test_logout():
    with client:
        client.cookies.set("session", "test_session")
        response = client.get("/logout")
        assert response.status_code == 200