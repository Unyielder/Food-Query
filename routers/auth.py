from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

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
    # <=0.15
    # user = await oauth.google.parse_id_token(request, token)
    # user = token['userinfo']
    user = token
    print(user)
    return user

