from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.params import Body
from typing import Optional, List
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .. import oauth2, schemas, models
from ..database import get_db

router = APIRouter( tags = ['Vote'])

@router.post('/votes', status_code=201)
def vote(vote:schemas.Vote, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    print('kk')
    post = db.query(models.Votes).filter(models.Votes.post_id == vote.id, models.Votes.user_id == current_user.id)

    if vote.direction == 0:
        if post.first():
            post.delete(synchronize_session=False)
            db.commit()
            return{"message": "It has been deleted."}
        
        else:
            raise HTTPException(status_code=404, detail="The post you're looking for doesn't exists.")
        
    elif vote.direction == 1:
        if post.first():
            raise HTTPException(status_code=409, detail="You have voted on this post already.")
        
        else:
            new_post = models.Votes(user_id =current_user.id, post_id = vote.id)
            db.add(new_post)
            db.commit()
            return {"message" : "We did it Joe"}


