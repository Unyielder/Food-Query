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
    # user = await oauth.google.parse_id_token(request, token)
    user = token['userinfo']
    # user = token
    # print(token)
    #print(user)
    #id_token
    request.session['user'] = user
    request.session['access_token'] = token['access_token']
    response = RedirectResponse(f'/dashboard')
    response.status_code = 302
    return response


@router.route('/dashboard')
async def dashboard(request: Request, ):
    print(request.session['user'])
    print(request.session['access_token'])
    return templates.TemplateResponse("userBookmarks.html", {"request": request})