from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from Food_Query.models import Bookmark


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/bookmarks')
async def get_bookmarks(request: Request):
    bookmarks = Bookmark.objects(id_token=request.session['id'])
    print(bookmarks)
    return templates.TemplateResponse("userBookmarks.html", {"request": request, "bookmarks": bookmarks})
