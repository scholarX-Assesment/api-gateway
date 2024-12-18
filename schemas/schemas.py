from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime


#Schemas for Student Service

class AcademicHistoryBase(BaseModel):
    year: int
    achievement: str

    @validator('year')
    def validate_year(cls, year):
        current_year = datetime.now().year
        if year > current_year:
            raise ValueError("Year cannot be in the future")
        return year


class AcademicHistoryCreate(AcademicHistoryBase):
    pass


class AcademicHistory(AcademicHistoryBase):
    id: int
    student_id: int

    class Config:
        orm_mode = True


class EnrolledCourseBase(BaseModel):
    course_id: int


class EnrolledCourseCreate(EnrolledCourseBase):
    pass


class EnrolledCourse(EnrolledCourseBase):
    id: int
    student_id: int

    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    name: str
    email: str
    address: str
    contactNo: str
    cgpa: float


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    academic_history: List[AcademicHistory] = []
    enrolled_courses: List[EnrolledCourse] = []

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    credits: float


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True



#Schemas for Notification Service

class EmailRequest(BaseModel):
    recipient: str
    content: str

class BulkEmailRequest(BaseModel):
    recipients: List[str]
    content: str



#Schemas for Class Schedule Service

class TeacherBase(BaseModel):
    name: str
    email: str
    subject: str
    contact_no: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int

    class Config:
        orm_mode = True

class ClassBase(BaseModel):
    name: str
    location: str

class ClassCreate(ClassBase):
    pass

class Class_(ClassBase):
    id: int

    class Config:
        orm_mode = True

class ClassScheduleBase(BaseModel):
    schedule_name: str
    teacher_id: int
    class_id: int 
    time_slot: str

class ClassScheduleCreate(ClassScheduleBase):
    pass

class ClassSchedule(ClassScheduleBase):
    id: int
    teacher: Teacher
    class_: Class_

    class Config:
        orm_mode = True