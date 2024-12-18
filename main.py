from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import requests
import schemas.schemas as schemas
from typing import List

app = FastAPI(title="API Gateway")

STUDENT_SERVICE_URL = "http://localhost:5001"
CLASS_SCHEDULE_SERVICE_URL = "http://localhost:5002"
EMAIL_SENDER_SERVICE_URL = "http://localhost:5003"


def forward_request(service_url, path, method="GET", body=None, params=None):
    url = f"{service_url}{path}"
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=body)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            raise ValueError("Unsupported HTTP method")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate):
    student_response = forward_request(STUDENT_SERVICE_URL, "/students/", method="POST", body=student.dict())
    
    email_request = {
        "recipient": student_response["email"],
        "content": f"Welcome, {student_response['name']}! Your account has been created for EduTrack."
    }
    forward_request(EMAIL_SENDER_SERVICE_URL, "/send-email/", method="POST", body=email_request)
    
    return student_response


@app.get("/students/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 10):
    return forward_request(STUDENT_SERVICE_URL, "/students/", method="GET", params={"skip": skip, "limit": limit})


@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int):
    return forward_request(STUDENT_SERVICE_URL, f"/students/{student_id}")


@app.delete("/students/{student_id}", response_model=schemas.Student)
def delete_student(student_id: int):
    return forward_request(STUDENT_SERVICE_URL, f"/students/{student_id}", method="DELETE")


@app.post("/students/{student_id}/academic-history/", response_model=schemas.AcademicHistory)
def add_academic_history(student_id: int, academic: schemas.AcademicHistoryCreate):
    return forward_request(STUDENT_SERVICE_URL, f"/students/{student_id}/academic-history/", method="POST", body=academic.dict())

@app.get("/students/{student_id}/academic-history/", response_model=List[schemas.AcademicHistory])
def get_academic_history(student_id: int):
    return forward_request(STUDENT_SERVICE_URL, f"/students/{student_id}/academic-history/", method="GET")

@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate):
    return forward_request(STUDENT_SERVICE_URL, "/courses/", method="POST", body=course.dict())

@app.get("/courses/{course_id}", response_model=schemas.Course)
def read_course(course_id: int):
    return forward_request(STUDENT_SERVICE_URL, f"/courses/{course_id}")

@app.get("/courses/", response_model=List[schemas.Course])
def read_courses(skip: int = 0, limit: int = 10):
    return forward_request(STUDENT_SERVICE_URL, "/courses/", method="GET", params={"skip": skip, "limit": limit})

@app.post("/students/{student_id}/enroll/", response_model=schemas.EnrolledCourse)
def enroll_student(student_id: int, course: schemas.EnrolledCourseCreate):
    return forward_request(STUDENT_SERVICE_URL, f"/students/{student_id}/enroll/", method="POST", body=course.dict())

@app.get("/students/{student_id}/courses/", response_model=List[schemas.Course])
def get_student_courses(student_id: int):
    return forward_request(STUDENT_SERVICE_URL, f"/students/{student_id}/courses/", method="GET")


#Class Schedule Endpoints


@app.post("/class_schedules/", response_model=schemas.ClassSchedule)
def create_class_schedule(schedule: schemas.ClassScheduleCreate):
    response = forward_request(CLASS_SCHEDULE_SERVICE_URL, "/class_schedules/", method="POST", body=schedule.dict())
    
    
    teacher_response = forward_request(CLASS_SCHEDULE_SERVICE_URL, f"/teachers/{schedule['teacher_id']}")
    teacher = teacher_response

    
    teacher_email_body = {
        "recipient": teacher["email"],
        "content": f"Dear {teacher['name']}, you have a new class scheduled at {schedule['time_slot']} for {schedule['schedule_name']}."
    }

    forward_request(EMAIL_SENDER_SERVICE_URL, "/send-email/", method="POST", body=teacher_email_body)
    
    return response

@app.get("/class_schedules/")
def read_class_schedules(skip: int = 0, limit: int = 10):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, "/class_schedules/", method="GET", params={"skip": skip, "limit": limit})


@app.get("/class_schedules/{schedule_id}", response_model=schemas.ClassSchedule)
def read_class_schedule(schedule_id: int):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, f"/class_schedules/{schedule_id}")


@app.delete("/class_schedules/{schedule_id}", response_model=list[schemas.ClassSchedule])
def delete_class_schedule(schedule_id: int):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, f"/class_schedules/{schedule_id}", method="DELETE")


@app.post("/teachers/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate):
    response = forward_request(CLASS_SCHEDULE_SERVICE_URL, "/teachers/", method="POST", body=teacher.dict())
    
    email_body = {
            "recipient": teacher["email"],
            "content": f"Welcome {teacher['name']}! You have been successfully registered as a teacher at EduTrack."
    }
    forward_request(EMAIL_SENDER_SERVICE_URL, "/send-email/", method="POST", body=email_body)
    
    return response

@app.get("/teachers/")
def read_teachers(skip: int = 0, limit: int = 10):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, "/teachers/", method="GET", params={"skip": skip, "limit": limit})


@app.get("/teachers/{teacher_id}", response_model=schemas.Teacher)
def read_teacher(teacher_id: int):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, f"/teachers/{teacher_id}", method="GET")


@app.delete("/teachers/{teacher_id}", response_model=schemas.Teacher)
def delete_teacher(teacher_id: int):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, f"/teachers/{teacher_id}", method="DELETE")


# Notification Service Endpoints

@app.post("/send-email/")
def send_email(email_request: schemas.EmailRequest):
    return forward_request(EMAIL_SENDER_SERVICE_URL, "/send-email/", method="POST", body=email_request.dict())


@app.post("/send-bulk-email/")
def send_bulk_email(bulk_email_request: schemas.BulkEmailRequest):
    return forward_request(EMAIL_SENDER_SERVICE_URL, "/send-bulk-email/", method="POST", body=bulk_email_request.dict())




@app.get("/")
def health_check():
    return {"message": "API Gateway is up and running"}
