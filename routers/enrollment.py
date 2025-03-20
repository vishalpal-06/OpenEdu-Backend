from pydantic import BaseModel
from utils.models import Enrollment,Course, User
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
    tags=["Enrollments"],
    prefix="/enrollment"
)



@app.get("/enrollment")
def get_enrollments(db: db_dependency):
    return db.query(Enrollment).all()


@app.post("/create_enrollment")
def create_enrollment(db: db_dependency, user:user_dependency, course_id: int):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    existing_enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.fk_user_id == user["id"], Enrollment.fk_course_id == course_id)
        .first()
    )
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already enrolled in this course"
        )
    
    enrollment_rec = Enrollment(
        fk_user_id = user["id"],
        fk_course_id = course_id
    )
    db.add(enrollment_rec)
    db.commit()
    return {"message": "Enrollment created successfully"}


@app.delete("/delete_enrollment")
def delete_enrollment(db:db_dependency, user:user_dependency, enrollment_id:int):
    enrollment = db.query(Enrollment).filter(Enrollment.enroll_id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with id {enrollment_id} not found"
        )
    
    if enrollment.fk_user_id == user["id"]:
        db.delete(enrollment)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You Have Not with id {enrollment_id}"
        )