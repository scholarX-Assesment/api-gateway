# API Gateway for Microservices

This project is an API gateway that integrates three microservices: Student Service, Class Schedule Service, and Notification Service. It handles requests and routes them to the appropriate service.

## Project Structure

```
api-gateway
├── src
│   ├── index.js                  # Entry point of the API gateway
│   ├── routes                    # Contains route definitions
│   │   ├── studentRoutes.js      # Routes for student operations
│   │   ├── classScheduleRoutes.js # Routes for class schedule operations
│   │   └── notificationRoutes.js  # Routes for notification operations
│   ├── controllers               # Contains request handling logic
│   │   ├── studentController.js   # Controller for student operations
│   │   ├── classScheduleController.js # Controller for class schedule operations
│   │   └── notificationController.js # Controller for notification operations
│   └── services                  # Contains service logic for each microservice
│       ├── studentService.js      # Service for student operations
│       ├── classScheduleService.js # Service for class schedule operations
│       └── notificationService.js  # Service for notification operations
├── package.json                  # NPM configuration file
└── README.md                     # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd api-gateway
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the API gateway:
   ```
   npm start
   ```

## API Usage

### Student Service

- **Create a Student**
  - **Endpoint:** POST /students
  - **Description:** Creates a new student.

- **Get Student by ID**
  - **Endpoint:** GET /students/{student_id}
  - **Description:** Retrieves a student by their ID.

- **Get All Students**
  - **Endpoint:** GET /students/
  - **Description:** Retrieves a list of all students.

### Class Schedule Service

- **Manage Class Schedules**
  - **Endpoints:** (To be defined)

### Notification Service

- **Send Notification**
  - **Endpoint:** POST /notifications
  - **Description:** Sends notifications, particularly for newly created students.

## License

This project is licensed under the MIT License.