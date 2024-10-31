from fastapi import HTTPException, APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuthError
from interface.auth.oauth_config import oauth

router = APIRouter()

@router.get("/")
def index():
    return {"message": "Bienvenido al sistema de autenticación con Google"}

@router.get("/login")
async def login(request: Request):
    if 'user' in request.session:
        return RedirectResponse(url=request.url_for('welcome'))
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)

@router.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        if user:
            request.session['user'] = dict(user)
            return RedirectResponse(url=request.url_for('welcome'))
        return {"message": "No se pudo obtener la información del usuario"}
    except OAuthError as e:
        return {"error": f"Error en la autenticación con Google: {e}"}

@router.get("/welcome")
async def welcome(request: Request):
    user = request.session.get('user')
    if user:
        return {"message": "Bienvenido a tu página"}
    raise HTTPException(status_code=401, detail="No autenticado")

@router.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url="/")
