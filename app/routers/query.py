import aiohttp
from fastapi import APIRouter, Request, HTTPException, Form
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from .service import *
import sys
sys.path.append('..')
from app.db.models import Bookmark
import asyncio


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/query")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/query")
async def search_food_desc(foodDescSearch: str = Form(...)) -> RedirectResponse:
    if not foodDescSearch.strip():
        raise HTTPException(status_code=404, detail="Error, no input")

    response = RedirectResponse(f'/query/{foodDescSearch}')
    response.status_code = 302
    return response


@router.get('/query/{user_input}')
async def get_food_desc(request: Request, user_input: str):
    foods = fuzzy_search(user_input)
    return templates.TemplateResponse("foodDescriptions.html", {"request": request, "user_input": user_input, "foods": foods})


@router.post('/query/{user_input}')
async def select_food_desc(foodName: str = Form(...)) -> RedirectResponse:
    food_code, food_desc = foodName.split(';')
    response = RedirectResponse(f'/query/{food_code}/{food_desc}/serving_size')
    response.status_code = 302
    return response


@router.get('/query/{food_code}/{food_desc}/serving_size')
async def get_servings(request: Request, food_code, food_desc):
    servings = await get_food_servings(food_code)
    return templates.TemplateResponse("foodServings.html", {"request": request, "food_desc": food_desc, "servings": servings})


@router.post('/query/{food_code}/{food_desc}/serving_size')
async def select_servings(food_code, food_desc, ing_measure: str = Form(...)):
    response = RedirectResponse(f'/query/{food_code}/{food_desc}/{ing_measure}')
    response.status_code = 302
    return response


@router.get('/query/{food_code}/{food_desc}/{serving_size}')
async def get_nutrients(request: Request, food_code, food_desc, serving_size):
    try:
        async with aiohttp.ClientSession() as session:
            async with asyncio.TaskGroup() as tg:
                task_amount = tg.create_task(get_food_data(session,
                    f"https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientamount/?id={food_code}&type=json&lang=en"))
                task_serving = tg.create_task(get_food_data(session,
                    f"https://food-nutrition.canada.ca/api/canadian-nutrient-file/servingsize/?id={food_code}&type=json&lang=en"))
                task_names = tg.create_task(get_food_data(session,
                    f"https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientname/?lang=en&type=json"))
                task_groups = tg.create_task(get_food_data(session,
                    f"https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientgroup/?lang=en&type=json"))

                df_amount = await task_amount
                df_serving = await task_serving
                df_names = await task_names
                df_groups = await task_groups

        df_food = df_amount.merge(df_names, left_on='nutrient_name_id', right_on='nutrient_name_id')
        df_food = df_food.merge(df_groups, left_on='nutrient_group_id', right_on='nutrient_group_id')
        df_food = df_food.merge(df_serving, left_on='food_code', right_on='food_code')

        df_food = df_food[df_food['measure_name'] == serving_size]
        df_food['serving_value'] = df_food.apply(lambda x: round(x['nutrient_value'] * x['conversion_factor_value'], 3), axis=1)
        df_food.sort_values(by='serving_value', inplace=True, ascending=False)

        df_aminos = df_food[df_food['nutrient_group_name'] == 'Amino Acids'].reset_index(drop=True)
        df_lipids = df_food[df_food['nutrient_group_name'] == 'Lipids'].reset_index(drop=True)
        # Converting grams into milligrams in lipids table
        df_lipids['serving_value'] = [val * 1000 if unit == 'g' else val for val, unit in zip(df_lipids['serving_value'], df_lipids['unit'])]
        df_lipids['unit'] = ['mg' for i in range(df_lipids.shape[0])]
        df_minerals = df_food[df_food['nutrient_group_name'] == 'Minerals'].reset_index(drop=True)
        df_carbs = df_food[df_food['nutrient_group_name'] == 'Other Carbohydrates'].reset_index(drop=True)
        df_other = df_food[df_food['nutrient_group_name'] == 'Other Components'].reset_index(drop=True)
        df_prox = df_food[df_food['nutrient_group_name'] == 'Proximates'].reset_index(drop=True)
        df_vita = df_food[df_food['nutrient_group_name'] == 'Vitamins'].reset_index(drop=True)
    except ValueError:
        raise HTTPException(404, "Couldn't find specific food data")

    is_bookmarked = None
    if 'user' in request.session:
        bookmark = Bookmark.objects(
            user_id=request.session['id'],
            food_code=food_code,
            food_desc=food_desc,
            serving_size=serving_size
        )
        if not bookmark:
            is_bookmarked = False
        else:
            is_bookmarked = True

    return templates.TemplateResponse("foodNutrients.html", {"request": request,
                                                             "food_desc": food_desc,
                                                             "serving_size": serving_size,
                                                             "df_food": df_food,
                                                             "df_aminos": df_aminos,
                                                             "df_lipids": df_lipids,
                                                             "df_minerals": df_minerals,
                                                             "df_carbs": df_carbs,
                                                             "df_other": df_other,
                                                             "df_prox": df_prox,
                                                             "df_vita": df_vita,
                                                             "is_bookmarked": is_bookmarked
                                                             })
