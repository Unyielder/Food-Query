from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from mongoengine import connect
import os
from routers import query
from routers import auth
from routers import bookmark
connect(db="FoodQueryDB", host="localhost", port=27017)

app = FastAPI()
app.include_router(query.router)
app.include_router(auth.router)
app.include_router(bookmark.router)


app.add_middleware(SessionMiddleware, secret_key=os.environ.get('GOOGLE_CLIENT_SECRET'))
root = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(root, 'static')), name="static")
templates = Jinja2Templates(directory="templates")
