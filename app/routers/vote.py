from fastapi import FastAPI, Response, responses, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import user
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from ..import models, schemas, database, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_User)):
    
    post_chk = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_chk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post does with id {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on voted on post {vote.post_id}")

        new_vote = models.Vote(post_id = vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message' : "voted successfully"}
                
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "vote does not exist")
  
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message' : "delted successfully"}