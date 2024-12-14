from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI(title="API Gateway")

STUDENT_SERVICE_URL = "http://student-service:5001"
CLASS_SCHEDULE_SERVICE_URL = "http://class-schedule-service:5002"
EMAIL_SENDER_SERVICE_URL = "http://notification-service:5003"


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



@app.post("/students/")
def create_student(student: dict):
    student_response = forward_request(STUDENT_SERVICE_URL, "/students/", method="POST", body=student)
    
    email_request = {
        "recipient": student_response["email"],
        "content": f"Welcome, {student_response['name']}! Your account has been created."
    }
    forward_request(EMAIL_SENDER_SERVICE_URL, "/send-email/", method="POST", body=email_request)
    
    return student_response


@app.get("/students/")
def read_students(skip: int = 0, limit: int = 10):
    return forward_request(STUDENT_SERVICE_URL, "/students/", method="GET", params={"skip": skip, "limit": limit})


@app.get("/students/{student_id}")
def read_student(student_id: int):
    return forward_request(STUDENT_SERVICE_URL, f"/students/{student_id}")


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    return forward_request(STUDENT_SERVICE_URL, f"/students/{student_id}", method="DELETE")




@app.post("/class_schedules/")
def create_class_schedule(schedule: dict):
    response = forward_request(CLASS_SCHEDULE_SERVICE_URL, "/class_schedules/", method="POST", body=schedule)
    
    
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


@app.get("/class_schedules/{schedule_id}")
def read_class_schedule(schedule_id: int):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, f"/class_schedules/{schedule_id}")


@app.delete("/class_schedules/{schedule_id}")
def delete_class_schedule(schedule_id: int):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, f"/class_schedules/{schedule_id}", method="DELETE")


@app.post("/teachers/")
def create_teacher(teacher: dict):
    response = forward_request(CLASS_SCHEDULE_SERVICE_URL, "/teachers/", method="POST", body=teacher)
    
    email_body = {
            "recipient": teacher["email"],
            "content": f"Welcome {teacher['name']}! You have been successfully registered as a teacher."
    }
    forward_request(EMAIL_SENDER_SERVICE_URL, "/send-email/", method="POST", body=email_body)
    
    return response

@app.get("/teachers/")
def read_teachers(skip: int = 0, limit: int = 10):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, "/teachers/", method="GET", params={"skip": skip, "limit": limit})


@app.get("/teachers/{teacher_id}")
def read_teacher(teacher_id: int):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, f"/teachers/{teacher_id}", method="GET")


@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    return forward_request(CLASS_SCHEDULE_SERVICE_URL, f"/teachers/{teacher_id}", method="DELETE")




@app.post("/send-email/")
def send_email(email_request: dict):
    return forward_request(EMAIL_SENDER_SERVICE_URL, "/send-email/", method="POST", body=email_request)


@app.post("/send-bulk-email/")
def send_bulk_email(bulk_email_request: dict):
    return forward_request(EMAIL_SENDER_SERVICE_URL, "/send-bulk-email/", method="POST", body=bulk_email_request)




@app.get("/")
def health_check():
    return {"message": "API Gateway is up and running"}
