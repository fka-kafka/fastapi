from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from . import models
from app.database import engine
from routers import posts, users, auth, votes

# models.Base.metadata.create_all(bind=engine) #commented out due to alembic being in use

app = FastAPI()

templates = Jinja2Templates(directory='templates')

origins = ['*']

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)


@app.get('/', response_class=HTMLResponse)
def landing_page(request: Request):
  
    return templates.TemplateResponse(
      request=request, name='landing_page.html'
    )

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
