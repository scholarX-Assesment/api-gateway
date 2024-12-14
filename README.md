# API Gateway

This API Gateway routes requests to the appropriate microservices: Student Service, Class Schedule Service, and Notification Service.

## Microservices

- **Student Service**: Runs on port `5001`
- **Class Schedule Service**: Runs on port `5002`
- **Notification Service**: Runs on port `5003`

## Endpoints

### Students

- **Create Student**
  - **POST** `/students/`
  - Request Body:
    ```json
    {
      "name": "string",
      "email": "string",
      "address": "string",
      "contactNo": "string",
      "cgpa": 0
    }
    ```

- **Get Student by ID**
  - **GET** `/students/{student_id}`

- **Get All Students**
  - **GET** `/students/`

- **Delete Student**
  - **DELETE** `/students/{student_id}`

### Class Schedules

- **Create Class Schedule**
  - **POST** `/class_schedules/`
  - Request Body:
    ```json
    {
      "teacher_id": "int",
      "student_id": "int",
      "time_slot": "string",
      "schedule_name": "string"
    }
    ```

- **Get Class Schedule by ID**
  - **GET** `/class_schedules/{schedule_id}`

- **Get All Class Schedules**
  - **GET** `/class_schedules/`

### Teachers

- **Create Teacher**
  - **POST** `/teachers/`
  - Request Body:
    ```json
    {
      "name": "string",
      "email": "string",
      "address": "string",
      "contactNo": "string"
    }
    ```

- **Get Teacher by ID**
  - **GET** `/teachers/{teacher_id}`

- **Get All Teachers**
  - **GET** `/teachers/`

- **Update Teacher**
  - **PUT** `/teachers/{teacher_id}`
  - Request Body:
    ```json
    {
      "name": "string",
      "email": "string",
      "address": "string",
      "contactNo": "string"
    }
    ```

- **Delete Teacher**
  - **DELETE** `/teachers/{teacher_id}`

## Notification

- **Send Email**
  - **POST** `/send-email/`
  - Request Body:
    ```json
    {
      "recipient": "string",
      "content": "string"
    }
    ```

## Running the API Gateway

1. Install dependencies:
   ```sh
   pip install -r requirements.txt