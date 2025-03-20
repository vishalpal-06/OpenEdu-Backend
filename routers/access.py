from fastapi import APIRouter ,Depends, HTTPException, status
from typing import Annotated
from pydantic import BaseModel
from utils.db_common import (
    authenticate_user,
    create_access_token,
    db_dependency
)
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

app = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type':'bearer'}


