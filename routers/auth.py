from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, oauth2, schemas
from app.database import get_db
from app.utils import verifier

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    query = db.query(models.User).filter(
        models.User.email == user_credentials.username)
    user = query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Email or Password"
                            )

    authenticated = verifier(user_credentials.password, user.password)

    if not authenticated:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Email or Password"
                            )

    access_token = oauth2.create_access_token(
        {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
