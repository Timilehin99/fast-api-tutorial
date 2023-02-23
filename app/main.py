from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, users, auth, votes
from pydantic import BaseSettings
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# models.Base.metadata.create_all(bind=engine)
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"messaege": "Welcome young scribe."}


