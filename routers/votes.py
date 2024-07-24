from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user


router = APIRouter(
  prefix='/vote',
  tags=['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def post_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    found_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post id: {vote.post_id} you have requested to vote for does not exist.")
    
    if (vote.vote_dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User of id {current_user.id} has already voted on post of id {vote.post_id}.")
        
        new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        
        return {"Response": "You have successfully voted for the post."}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote was not found.")
          
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Response": "Vote has been successfully deleted."}