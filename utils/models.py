from utils.database import Base
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    ForeignKey,
    Enum,
    UniqueConstraint,
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    role = Column(Enum("learner", "creator", name="user_role"), nullable=False)


class Course(Base):
    __tablename__ = 'course'

    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, unique=True)
    course_duration = Column(Integer)
    creator_id = Column(Integer, ForeignKey(User.id))


class Enrollment(Base):
    __tablename__ = 'enrollment'

    enroll_id = Column(Integer, primary_key=True, index=True)
    fk_user_id = Column(Integer, ForeignKey(User.id))
    fk_course_id = Column(Integer, ForeignKey(Course.course_id))

    __table_args__ = (UniqueConstraint("fk_user_id", "fk_course_id", name="uq_user_course"),)