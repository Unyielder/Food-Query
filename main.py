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
    user_input = form.get("foodName")
    foods = fuzzy_search(user_input)
    foods = json.dumps(foods)

    response = RedirectResponse(f'/query/{foods}')
    response.status_code = 302
    return response


@app.get('/query/{foods}')
async def select_food_desc(request: Request, foods: str):
    foods = json.loads(foods)
    return templates.TemplateResponse("foodNames.html", {"request": request, "foods": foods})
