from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from utils import *

root = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(root, 'static')), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/query")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/query")
async def search_food_desc(request: Request) -> RedirectResponse:
    form = await request.form()
    user_input = form.get("foodDescSearch")

    response = RedirectResponse(f'/query/{user_input}')
    response.status_code = 302
    return response


@app.get('/query/{user_input}')
async def get_food_desc(request: Request, user_input: str):
    foods = fuzzy_search(user_input)
    return templates.TemplateResponse("foodDescriptions.html", {"request": request, "user_input": user_input, "foods": foods})


@app.post('/query/{user_input}')
async def select_food_desc(request: Request):
    form = await request.form()
    food_code, food_desc = form.get('foodName').split(';')
    response = RedirectResponse(f'/query/{food_code}/{food_desc}/serving_size')
    response.status_code = 302
    return response


@app.get('/query/{food_code}/{food_desc}/serving_size')
async def get_servings(request: Request, food_code, food_desc):
    res = requests.get(f'https://food-nutrition.canada.ca/api/canadian-nutrient-file/servingsize/?id={food_code}&type'
                       f'=json&lang=en')
    servings = res.json()
    print(servings)
    return templates.TemplateResponse("foodServings.html", {"request": request, "food_desc": food_desc, "servings": servings})


@app.post('/query/{food_code}/{food_desc}/serving_size')
async def select_servings(request: Request, food_code, food_desc):
    form = await request.form()
    serving_size = form.get('ing_measure')
    response = RedirectResponse(f'/query/{food_code}/{food_desc}/{serving_size}')
    response.status_code = 302
    return response


@app.get('/query/{food_code}/{food_desc}/{serving_size}')
async def get_nutrients(request: Request, food_code, food_desc, serving_size):
    df_amount = get_food_data(f"https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientamount/?id={food_code}&type=json&lang=en")
    df_amount = df_amount[['food_code', 'nutrient_value', 'nutrient_name_id', 'nutrient_web_name']]
    df_serving = get_food_data(f"https://food-nutrition.canada.ca/api/canadian-nutrient-file/servingsize/?id={food_code}&type=json&lang=en")
    df_serving = df_serving[['food_code', 'conversion_factor_value', 'measure_name']]
    df_names = get_food_data(f"https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientname/?lang=en&type=json")
    df_names = df_names[['nutrient_name_id', 'nutrient_web_name', 'unit', 'nutrient_group_id']]
    df_groups = get_food_data(f"https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientgroup/?lang=en&type=json")
    df_groups = df_groups[['nutrient_group_id', 'nutrient_group_name']]

    df_food = df_amount.merge(df_names, left_on='nutrient_name_id', right_on='nutrient_name_id')
    df_food = df_food.merge(df_groups, left_on='nutrient_group_id', right_on='nutrient_group_id')
    df_food = df_food.merge(df_serving, left_on='food_code', right_on='food_code')

    df_food = df_food[df_food['measure_name'] == test_session['food'].serving_size]
    df_food['serving_value'] = df_food.apply(lambda x: round(x['nutrient_value'] * x['conversion_factor_value'], 2), axis=1)
    df_food.sort_values(by='serving_value', inplace=True, ascending=False)

    df_aminos = df_food[df_food['nutrient_group_name'] == 'Amino Acids'].reset_index(drop=True)
    df_lipids = df_food[df_food['nutrient_group_name'] == 'Lipids'].reset_index(drop=True)
    df_minerals = df_food[df_food['nutrient_group_name'] == 'Minerals'].reset_index(drop=True)
    df_carbs = df_food[df_food['nutrient_group_name'] == 'Other Carbohydrates'].reset_index(drop=True)
    df_other = df_food[df_food['nutrient_group_name'] == 'Other Components'].reset_index(drop=True)
    df_prox = df_food[df_food['nutrient_group_name'] == 'Proximates'].reset_index(drop=True)
    df_vita = df_food[df_food['nutrient_group_name'] == 'Vitamins'].reset_index(drop=True)
    print(df_food)
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
                                                             "df_vita": df_vita
                                                             })

