from fastapi import HTTPException, APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from authlib.integrations.starlette_client import OAuthError
from interface.auth.oauth_config import oauth

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/login")
async def login(request: Request):
    if 'user' in request.session:
      
        return RedirectResponse(url=request.url_for('inicio'))
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)

@router.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        if user:
           
            request.session['user'] = dict(user)
            
            return RedirectResponse(url=request.url_for('inicio'))
        return {"message": "No se pudo obtener la información del usuario"}
    except OAuthError as e:
        return {"error": f"Error en la autenticación con Google: {e}"}

@router.get("/inicio", name="inicio")
async def welcome(request: Request):
    user = request.session.get('user')
    if user:
       
        return templates.TemplateResponse("home.html", {"request": request})
    
    raise HTTPException(status_code=401, detail="No autenticado")

@router.get("/logout")
async def logout(request: Request):
    
    request.session.pop('user', None)
    return RedirectResponse(url="/")