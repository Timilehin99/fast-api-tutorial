from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.params import Body
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from .. import oauth2


router = APIRouter(tags = ['Authentication'])

@router.post('/login', response_model = schemas.Token)
def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    new_post = db.query(models.Users).filter(models.Users.email == creds.username).first()

    if new_post:
        if utils.verify(creds.password, new_post.password):
            access_token = oauth2.create_jwt_token(data = {'user_id': new_post.id})

            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=403, detail = 'The credentials are not correct')
    else:
        raise HTTPException(status_code=403, detail='The credentials are not correct.')
