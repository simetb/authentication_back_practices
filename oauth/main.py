"""
    FastAPI
    OAuth2 github implementation and user info retrieval
"""
import requests
from requests_oauthlib import OAuth2Session
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import urlparse, parse_qs
import os

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'
USER_INFO_URL = 'https://api.github.com/user'

github = OAuth2Session(CLIENT_ID, redirect_uri='http://localhost:8000/callback')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Original Api route
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
        <h1>Your API works fine :D</h1>
    """

# Route for the login page with github authorization
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    authorization_url, state = github.authorization_url(AUTHORIZATION_BASE_URL)
    return templates.TemplateResponse("login.html", {"request": request, "authorization_url": authorization_url})

# Route for the callback after the user has authorized the app
@app.get("/callback")
async def callback(request: Request, code: str):
    # Verify the authorization code
    if code:
        token = github.fetch_token(TOKEN_URL, code=code, client_secret=CLIENT_SECRET)
        # Here you can save the session or user data
        return RedirectResponse(url="/success")
    else:
        return "Error: No authorization code received."

# Route for the success page after the user has been authenticated
@app.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    # Get user information
    response = github.get(USER_INFO_URL)
    user_info = response.json()
    return templates.TemplateResponse("user_info.html", {"request": request, "user_info": user_info})
