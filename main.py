from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from routers import query


app = FastAPI()
app.include_router(query.router)

app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
root = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(root, 'static')), name="static")
templates = Jinja2Templates(directory="templates")
