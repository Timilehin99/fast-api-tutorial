from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.params import Body
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import Optional

router = APIRouter(tags=['Users'])



@router.get("/post", status_code = 200, response_model = List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit:int = 10, skip : int = 0, search: Optional[str] = ""):
    # cursor.execute('''SELECT * FROM posts''')
    # my_post = cursor.fetchall()

    my_post = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

    optimized_post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    return optimized_post

@router.get("/post/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(f'''SELECT * FROM posts WHERE id ={id}''')
    # post = cursor.fetchone()
    # if (post):
    #     return(post)
    # else:
    #     return('The record could not be found')
    new_post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if new_post:
        return new_post
    else:
        raise HTTPException(status_code=404, detail = f'User with ID:{id} was not found.')

@router.post("/post", status_code=201, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):  
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
    #     RETURNING *''', (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()
    # return(post)

    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return (new_post)

@router.delete("/post/{id}", status_code=204) 
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id)))
    # p = cursor.fetchone()
    # conn.commit()

    p = db.query(models.Post).filter(models.Post.id == id)
    
    if(p.first()):
        if (p.first().user_id != current_user.id):
            raise HTTPException(status_code = 403, detail= 'You do not have the authority to delete this post.')
        
        p.delete(synchronize_session = False)
        db.commit()
    else:
        raise HTTPException(status_code=400, 
                detail=f'Post {id} no dey there oga. No dey stress me.')

@router.put("/post/{id}", status_code=200, response_model=schemas.PostResponse)
def update_post(id:int, post:schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    # p = cursor.fetchone()
    # conn.commit()
    p = db.query(models.Post).filter(models.Post.id == id)

    if(p.first()):
        if (p.first().user_id != current_user.id):
            raise HTTPException(status_code = 403, detail= 'You do not have the authority to delete this post.')
        
        p.update(post.dict(), synchronize_session=False)
        db.commit()

        return p.first()

    else:
        raise HTTPException(status_code=404, 
                detail=f'Post {id} no dey there oga. No dey stress me.')
