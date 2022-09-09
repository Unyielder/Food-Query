from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from Food_Query.models import Bookmark


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/bookmarks')
async def get_bookmarks(request: Request):
    bookmarks = Bookmark.objects(user_id=request.session['id'])
    return templates.TemplateResponse("userBookmarks.html", {"request": request, "bookmarks": bookmarks})


@router.post('/bookmarks/delete/{id_bookmark}', status_code=204)
async def delete_bookmark(request: Request, id_bookmark):
    bookmark = Bookmark.objects(
        id=id_bookmark
    )
    if bookmark:
        bookmark.delete()

    response = RedirectResponse('/bookmarks')
    response.status_code = 302
    return response
