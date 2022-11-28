from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from app.db.models import Bookmark


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/bookmarks')
async def get_bookmarks(request: Request):
    bookmarks = Bookmark.objects(user_id=request.session['id'])
    return templates.TemplateResponse("userBookmarks.html", {"request": request, "bookmarks": bookmarks})


@router.post('/query/{food_code}/{food_desc}/{serving_size}', status_code=204)
async def save_to_bookmarks(request: Request, food_code, food_desc, serving_size):
    if 'user' in request.session:
        bookmark = Bookmark.objects(
            user_id=request.session['id'],
            food_code=food_code,
            food_desc=food_desc,
            serving_size=serving_size
        ).first()

        if bookmark is None:
            Bookmark(
                user_id=request.session['id'],
                food_code=food_code,
                food_desc=food_desc,
                serving_size=serving_size
            ).save()

        response = RedirectResponse(f'/query/{food_code}/{food_desc}/{serving_size}')
        response.status_code = 302
        return response

    else:
        bookmark_dict = {
            'food_code': food_code,
            'food_desc': food_desc,
            'serving_size': serving_size
        }

        request.session['bookmark_to_save'] = bookmark_dict
        response = RedirectResponse(f'/login')
        response.status_code = 302
        return response


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
