from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.params import Body
from typing import Optional, List
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .. import utils
from .. import models, schemas
from ..database import get_db



router = APIRouter(tags=['Users'])

@router.post("/users", status_code=201, response_model=schemas.UserResponse)
def create_user(post: schemas.CreateUser, db: Session = Depends(get_db)):  
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
    #     RETURNING *''', (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()
    # return(post)
    post.password = utils.hashie(post.password)
    new_post = models.Users(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return (new_post)

@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(f'''SELECT * FROM posts WHERE id ={id}''')
    # post = cursor.fetchone()
    # if (post):
    #     return(post)
    # else:
    #     return('The record could not be found')
    new_post = db.query(models.Users).filter(models.Users.id == id).first()

    if new_post:
        return new_post
    else:
        raise HTTPException(status_code=404, detail = f'User with ID:{id} was not found.')
