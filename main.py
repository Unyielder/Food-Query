from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import *
import json


app = FastAPI()
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
    return templates.TemplateResponse("foodDescriptions.html", {"request": request, "foods": foods})


@app.post('/query/{user_input}')
async def select_food_desc(request: Request, user_input: str):
    form = await request.form()
    food_code = form.get('foodName')

    response = RedirectResponse(f'/query/{user_input}/{food_code}')
    response.status_code = 302
    return response


@app.get('/query/{user_input}/{food_code}')
async def get_servings(request: Request, user_input: str, food_code):
    res = requests.get(f'https://food-nutrition.canada.ca/api/canadian-nutrient-file/servingsize/?id={food_code}&type'
                       f'=json&lang=en')

    servings = res.json()
    print(servings)
    return templates.TemplateResponse("foodServings.html", {"request": request, "servings": servings})

















