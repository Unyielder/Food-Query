from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/query")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/query")
async def search_food_desc(request: Request):
    form = await request.form()
    foods = form.get("foodName")
    print(foods)
    res = requests.get("https://food-nutrition.canada.ca/api/canadian-nutrient-file/food/?lang=en&type=json")
    foods = res.json()
    return templates.TemplateResponse("foodNames.html", {"request": request, "foods": foods})
