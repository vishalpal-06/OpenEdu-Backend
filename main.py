from fastapi import FastAPI
from routers import (
    user,
    course,
    enrollment,
    access,
)
from utils.database import engine
from utils import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user.app)
app.include_router(course.app)
app.include_router(enrollment.app)
app.include_router(access.app)

