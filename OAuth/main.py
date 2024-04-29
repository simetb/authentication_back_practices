import requests
from requests_oauthlib import OAuth2Session
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import urlparse, parse_qs

CLIENT_ID = 'b28f8e87e82ac98ef8f1'
CLIENT_SECRET = '2469a4723028c136879483f8042498941a579637'
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'
USER_INFO_URL = 'https://api.github.com/user'

github = OAuth2Session(CLIENT_ID, redirect_uri='http://localhost:8000/callback')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Ruta principal de la API
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
        <h1>Your API works fine :D</h1>
    """

# Ruta para iniciar el flujo de OAuth
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    authorization_url, state = github.authorization_url(AUTHORIZATION_BASE_URL)
    return templates.TemplateResponse("login.html", {"request": request, "authorization_url": authorization_url})

# Ruta de redirección después de la autorización
@app.get("/callback")
async def callback(request: Request, code: str):
    # Verificar si se recibió el código de autorización
    if code:
        token = github.fetch_token(TOKEN_URL, code=code, client_secret=CLIENT_SECRET)
        # Aquí puedes guardar el token en la sesión del usuario o en la base de datos
        return RedirectResponse(url="/success")
    else:
        return "Error: No authorization code received."

@app.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    # Obtener información del usuario autenticado
    response = github.get(USER_INFO_URL)
    user_info = response.json()
    # Renderizar la plantilla con la información del usuario
    return templates.TemplateResponse("user_info.html", {"request": request, "user_info": user_info})
