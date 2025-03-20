from fastapi import Depends, HTTPException, status
from database import sessionlocal
from typing import Annotated
from models import User
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = 'd2e2b8fe4827c93ad7ac831a45b2f28c6f33e04f975c0b4b2b1b8d8b38d694a4'
ALGORITHUM = 'HS256'
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/token')


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if bcrypt_context.verify(password, user.hashed_password):
        return user
    return False


def create_access_token(username:str, user_id: int, expries_delta: timedelta):
    encode = {
        'sub': username, 
        'id': user_id
    }
    expires = datetime.now(timezone.utc) + expries_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHUM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHUM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Cloud Not Validate User.')
        return {'username': username, 'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Cloud Not Validate User.')


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]