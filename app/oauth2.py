from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from app import schemas, models
from app.config import settings
from app.database import get_db
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_TIME = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expiry = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_TIME)
    to_encode.update({"exp": expiry})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str | None = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials.", headers={"WWW-Authenticate": "Bearer"}
                                          )
    payload_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(
        models.User.id == payload_data.id).first()

    return user
