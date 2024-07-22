from fastapi import status, HTTPException, Depends, APIRouter
from app import models, schemas
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils import hasher

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

#############################
# Path Operations for Users #
#############################

### Create User ###
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Password hashing
    hashed_passwd = hasher(user.password)
    user.password = hashed_passwd

    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


### Get specific user ###
@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {
                            id} was not found. User might not exist."
                            )

    return user
