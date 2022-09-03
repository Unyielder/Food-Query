from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/bookmarks')
async def dashboard(request: Request):
    return templates.TemplateResponse("userBookmarks.html", {"request": request})
