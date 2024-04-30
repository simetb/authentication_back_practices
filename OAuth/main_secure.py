"""
    FastAPI
    OAuth2 github implementation and protected routes example
    with the validation of the token.
"""
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from requests_oauthlib import OAuth2Session
import os

app = FastAPI()

# Github credentials Oauth config
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/callback'
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to get the current user from the
async def get_current_user(authorization: str = Header(...)):
    if authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1]
        github = OAuth2Session(CLIENT_ID)
        try:
            # Verify the user's token
            user_info = github.get('https://api.github.com/user', headers={'Authorization': f'Bearer {token}'})
            if user_info.status_code == 200:
                # Valid token, return the user's login name
                return user_info.json().get('login')
            else:
                # Invalid token
                raise HTTPException(status_code=401, detail="Invalid access token")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error while validating access token")
    else:
        raise HTTPException(status_code=401, detail="No access token provided")

# Protected route with OAuth2 authentication
@app.get("/secure-route")
async def secure_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! You have access to this route."}
