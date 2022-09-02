from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.route('/bookmarks')
async def dashboard(request: Request):
    print(request.session['user'])
    return templates.TemplateResponse("userBookmarks.html", {"request": request})
