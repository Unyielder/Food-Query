from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

config = Config('.env')  # read config from .env file
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.route('/login')
async def login(request: Request):
    # absolute url for callback
    # we will define it below
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.route('/auth')
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    request.session['user'] = token['userinfo']
    request.session['id'] = token['id_token']
    response = RedirectResponse(f'/dashboard')
    response.status_code = 302
    return response


@router.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    request.session.pop('id', None)
    return RedirectResponse('/query')


@router.route('/dashboard')
async def dashboard(request: Request):
    print(request.session['user'])
    return templates.TemplateResponse("userBookmarks.html", {"request": request})