from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from .utils import hasher
from routers import posts, users, auth
# from fastapi.params import Body
# from psycopg import cursor
# import time
# import psycopg
# from random import randrange

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

# Initializing database connection via DB Driver (Accompanying code snippets also commented out)
# while True:
#     try:
#         connection = psycopg.connect(
#             "user=postgres dbname=fastapi host=localhost")
#         cursor = connection.cursor()
#         print("Database connection was succesful.")
#         break
#     except Exception as error:
#         print("Failed to connect to specified database:\n")
#         raise error
#         time.sleep(2)

#############################
# CRUD Operations for Posts #
#############################

# Root Path
# @app.get('/')
# def root():
#     return {"fastapi"}


### Create a post ###
# @app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
#     # cursor.execute("""
#     #                INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
#     #                """, (post.title, post.content, post.published))
#     # new_post = cursor.fetchone()
#     # connection.commit()

#     new_post = models.Post(
#         # title=post.title, content=post.content, published=post.published
#         **post.model_dump()
#     )

#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post


### Get all posts ###
# @app.get('/posts', response_model=List[schemas.PostResponse])
# def get_posts(db: Session = Depends(get_db)):
#     # cursor.execute("""
#     #                SELECT * FROM posts where id > 90
#     #                """)
#     # posts = cursor.fetchall()

#     all_posts = db.query(models.Post).all()

#     return all_posts


# ### Get a specific post ###
# @app.get('/posts/{id}', response_model=schemas.PostResponse)
# def get_post(id: int, db: Session = Depends(get_db)):
#     # cursor.execute("""
#     #                SELECT * FROM posts WHERE id = %s
#     #                """, [str(id)])
#     # post = cursor.fetchone()

#     query = db.query(models.Post).filter(models.Post.id == id)
#     reqested_post = query.first()

#     if not reqested_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"The post with id: {id} was not found"
#                             )

#     return reqested_post


# ### Update a post ###
# @app.put('/posts/{id}', response_model=schemas.PostResponse)
# def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
#     # cursor.execute("""
#     #                UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
#     #                """, [post.title, post.content, post.published, str(id)],)
#     # updated_post = cursor.fetchone()
#     # connection.commit()

#     query = db.query(models.Post).filter(models.Post.id == id)
#     updated_post = query.first()

#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"The post with id: {id} was not found"
#                             )

#     query.update(post.model_dump(), synchronize_session=False)
#     db.commit()

#     return updated_post


# ### Delete a post ###
# @app.delete('/posts/{id}')
# def delete_post(id: int, db: Session = Depends(get_db)):
#     # cursor.execute("""
#     #                DELETE FROM posts WHERE id = %s RETURNING *
#     #                """, [str(id)])
#     # deleted_post = cursor.fetchone()
#     # connection.commit()

#     query = db.query(models.Post).filter(models.Post.id == id)

#     if query.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"The post with id: {id} was not found"
#                             )

#     deleted_post = query.delete(synchronize_session=False)
#     db.commit()

#     return (f"Deleted post id: {id} has been deleted")


# #############################
# # CRUD Operations for Users #
# #############################

# ### Create new user ###
# @app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

#     # Password hashing
#     hashed_passwd = hasher(user.password)
#     user.password = hashed_passwd

#     new_user = models.User(**user.model_dump())

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


# ### Get specific user ###
# @app.get('/users/{id}', response_model=schemas.UserResponse)
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {
#                             id} was not found. User might not exist."
#                             )
#     return user
