from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from requests_oauthlib import OAuth2Session

app = FastAPI()

# Configuración de GitHub OAuth
CLIENT_ID = 'b28f8e87e82ac98ef8f1'
CLIENT_SECRET = '2469a4723028c136879483f8042498941a579637'
REDIRECT_URI = 'http://localhost:8000/callback'
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para validar la sesión de GitHub
async def get_current_user(authorization: str = Header(...)):
    if authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1]
        github = OAuth2Session(CLIENT_ID)
        try:
            # Verificar si el token es válido haciendo una solicitud a la API de GitHub
            user_info = github.get('https://api.github.com/user', headers={'Authorization': f'Bearer {token}'})
            if user_info.status_code == 200:
                # El token es válido, devuelve el nombre de usuario
                return user_info.json().get('login')
            else:
                # El token no es válido, devuelve un error HTTP
                raise HTTPException(status_code=401, detail="Invalid access token")
        except Exception as e:
            # Ocurrió un error al verificar el token
            raise HTTPException(status_code=500, detail="Error while validating access token")
    else:
        # No se proporcionó un token de acceso
        raise HTTPException(status_code=401, detail="No access token provided")

# Ruta protegida que requiere autenticación de GitHub
@app.get("/secure-route")
async def secure_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! You have access to this route."}
