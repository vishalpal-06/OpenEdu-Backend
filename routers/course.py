from pydantic import BaseModel
from utils.models import User,Course
from utils.models import User,Course
from utils.db_common import (
    db_dependency, 
    bcrypt_context,
    user_dependency
)
from fastapi import (
    APIRouter, 
    status,
    HTTPException,
)
from typing import Literal

app = APIRouter(
    tags=["Courses"],
    prefix="/courses"
)



@app.get("/course")
def get_courses(db: db_dependency):
    return db.query(Course).all()


class CourseRequest(BaseModel):
    course_name: str
    course_duration: int

@app.post("/create_course")
def create_course(db: db_dependency, user: user_dependency, create_course_request: CourseRequest):
    create_course_model = Course(
        course_name = create_course_request.course_name,
        course_duration = create_course_request.course_duration,
        creator_id = user["id"]
    )
    db.add(create_course_model)
    db.commit()
    

@app.put("/update_course")
def update_course(db:db_dependency, user:user_dependency, update_course_request:CourseRequest, course_id:int):
    update_course_model = db.query(Course).filter(Course.course_id == course_id).filter(Course.creator_id == user['id']).first()
    update_course_model.course_name = update_course_request.course_name
    update_course_model.course_duration = update_course_request.course_duration
    db.add(update_course_model)
    db.commit()


@app.delete("/delete_course/{course_name}")
def delete_course(db: db_dependency, user: user_dependency, course_name:str):
    course_name = db.query(Course).filter(Course.course_name == course_name).filter(Course.creator_id == user['id']).first()
    if course_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You don't have any course with name '{course_name}'"
        )
    db.delete(course_name)
    db.commit()
