from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from Food_Query.models import User, Bookmark

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
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.route('/auth')
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    request.session['user'] = token['userinfo']

    user = User.objects(email=token['userinfo']['email']).first()
    if user is None:  # new user
        user = User(
            id_token=token['id_token'],
            email=token['userinfo']['email'],
            first_name=token['userinfo']['given_name'],
            last_name=token['userinfo']['family_name'],
            profile_url=token['userinfo']['picture']
        ).save()

    request.session['id'] = str(user.id)

    if 'bookmark_to_save' in request.session:
        food_code = request.session['bookmark_to_save']['food_code']
        food_desc = request.session['bookmark_to_save']['food_desc']
        serving_size = request.session['bookmark_to_save']['serving_size']

        Bookmark(
            user_id=request.session['id'],
            food_code=food_code,
            food_desc=food_desc,
            serving_size=serving_size
        ).save()
        del request.session['bookmark_to_save']
        response = RedirectResponse(f'/query/{food_code}/{food_desc}/{serving_size}')

    else:  # regular login
        response = RedirectResponse(f'/bookmarks')

    response.status_code = 302
    return response


@router.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    request.session.pop('id', None)
    return RedirectResponse('/query')
