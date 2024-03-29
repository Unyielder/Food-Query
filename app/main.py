from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from mongoengine import connect
import sys
import os
sys.path.append('..')
from app.routers import query, auth
from app.routers import bookmark
from dotenv import load_dotenv
import certifi
load_dotenv()
connect(host=os.environ.get("MONGODB_URI", None))#, tlsCAFile=certifi.where())

app = FastAPI()
app.include_router(query.router)
app.include_router(auth.router)
app.include_router(bookmark.router)


app.add_middleware(SessionMiddleware, secret_key='a')#os.environ.get('GOOGLE_CLIENT_SECRET'))
root = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(root, 'static')), name="static")
templates = Jinja2Templates(directory="templates")
