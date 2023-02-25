from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import Settings

oaut_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# Expiration time

# To get a random 32 bit code "openssl rand -hex 32" use this in terminal

SECRET_KEY = Settings.secret_key # this is for a simple example
ALGORITHM = Settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(Settings.access_token_expire_minute)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, crediantials_exceptions):
    try:
        payload =  jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise crediantials_exceptions

        token_data  = schemas.Token_data(id = id)
    except JWTError as e:
        raise crediantials_exceptions
    return token_data

    
def get_current_user(token: str = Depends(oaut_scheme), db: Session = Depends(database.get_db)):
    crediantials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"couldnot validate crediantials",
                                            headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, crediantials_exceptions)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user