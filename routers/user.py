
from pydantic import BaseModel
from models import User
from common_func import (
    db_dependency, 
    bcrypt_context,
    user_dependency
)
from fastapi import (
    APIRouter, 
    status
)
from typing import Literal


app = APIRouter(
    tags=["Users"],
    prefix="/users"
)


@app.get("/users")
def get_users(db: db_dependency):
    return db.query(User).all()


class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: Literal["learner", "creator"]


@app.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_requiest: CreateUserRequest, db: db_dependency):
    create_user_model = User(
        email = create_user_requiest.email,
        username = create_user_requiest.username,
        first_name = create_user_requiest.first_name,
        last_name = create_user_requiest.last_name,
        hashed_password = bcrypt_context.hash(create_user_requiest.password),
        role = create_user_requiest.role
    )
    db.add(create_user_model)
    db.commit()


class UpdateUserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str


@app.put("/update_user")
def update_user(db: db_dependency, user:user_dependency, update_request: UpdateUserRequest):
    
    update_user_model = db.query(User).filter(User.id == user["id"]).first()
    
    update_user_model.username = update_request.username
    update_user_model.first_name = update_request.first_name
    update_user_model.last_name = update_request.last_name
    update_user_model.password = bcrypt_context.hash(update_request.password)

    db.add(update_user_model)
    db.commit()


@app.delete("/delete_user/")
async def delete_user(db: db_dependency, user:user_dependency):

    db.query(User).filter(User.id == user["id"]).delete()
    db.commit()