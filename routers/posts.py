from argparse import OPTIONAL
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, oauth2
from app.database import get_db


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


#############################
# Path Operations for Posts #
#############################

### Create a post ###
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #                INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
    #                """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    new_post = models.Post(
        # title=post.title, content=post.content, published=post.published
        creator_id=current_user.id, **post.model_dump()
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


### Get all posts ###
@router.get('/', response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 2, search: Optional[str] = ""):
    # cursor.execute("""
    #                SELECT * FROM posts where id > 90
    #                """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


### Get a specific post ###
@router.get('/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""
    #                SELECT * FROM posts WHERE id = %s
    #                """, [str(id)])
    # post = cursor.fetchone()

    query = db.query(models.Post).filter(models.Post.id == id)
    reqested_post = query.first()

    if not reqested_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id: {id} was not found"
                            )

    return reqested_post


### Update a post ###
@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #                UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
    #                """, [post.title, post.content, post.published, str(id)],)
    # updated_post = cursor.fetchone()
    # connection.commit()
    query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id: {id} was not found"
                            )

    if current_user.id != updated_post.creator_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are NOT authorized to perform the requested action."
                            )

    query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return updated_post


### Delete a post ###
@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #                DELETE FROM posts WHERE id = %s RETURNING *
    #                """, [str(id)])
    # deleted_post = cursor.fetchone()
    # connection.commit()
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id: {id} was not found"
                            )

    if current_user.id != post.creator_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are NOT authorized to perform the requested action."
                            )

    query.delete(synchronize_session=False)
    db.commit()

    return (f"Deleted post id: {id} has been deleted")
