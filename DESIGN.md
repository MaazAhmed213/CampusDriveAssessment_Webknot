# DESIGN.md

## Campus Event Management Platform Design Document

### 1. Assumptions & Decisions
- **Assumptions:**
  - The platform will initially support a single campus but should be scalable to multiple campuses.
  - SQLite is chosen for its simplicity and ease of use during the prototype phase.
  - The system will handle a moderate number of concurrent users typical for a campus environment.
  - Events can be created and managed by admin staff only.
  - Students can register for events, mark attendance, and provide feedback through the mobile app.
  - Feedback is collected as a rating from 1 to 5.

- **Decisions:**
  - Use RESTful APIs for communication between the mobile app and the backend.
  - Implement a simple authentication mechanism for students and admin staff.
  - Use Streamlit for a simple UI to display reports.

### 2. Data to Track
- **Event Creation:**
  - Event ID, Name, Description, Date, Time, Location, Created By (Admin ID).

- **Student Registration:**
  - Registration ID, Student ID, Event ID, Registration Timestamp.

- **Attendance:**
  - Attendance ID, Student ID, Event ID, Check-in Timestamp.

- **Feedback:**
  - Feedback ID, Student ID, Event ID, Rating (1-5), Feedback Timestamp.

### 3. Database Schema

#### Tables

- **Colleges**
  - `college_id` (Primary Key)
  - `name`
  - `location`

- **Students**
  - `student_id` (Primary Key)
  - `name`
  - `email` (Unique)
  - `college_id` (Foreign Key)

- **Events**
  - `event_id` (Primary Key)
  - `name`
  - `description`
  - `date`
  - `time`
  - `location`
  - `created_by` (Admin ID)

- **Registrations**
  - `registration_id` (Primary Key)
  - `student_id` (Foreign Key)
  - `event_id` (Foreign Key)
  - `timestamp`

- **Attendance**
  - `attendance_id` (Primary Key)
  - `student_id` (Foreign Key)
  - `event_id` (Foreign Key)
  - `check_in_timestamp`

- **Feedback**
  - `feedback_id` (Primary Key)
  - `student_id` (Foreign Key)
  - `event_id` (Foreign Key)
  - `rating`
  - `timestamp`

### 4. API Design

#### Endpoints

- **Register Student**
  - **Method:** POST
  - **URL:** `/api/students/register`
  - **Request:** `{ "name": "John Doe", "email": "john@example.com", "college_id": 1 }`
  - **Response:** `{ "student_id": 123, "message": "Registration successful" }`

- **Mark Attendance**
  - **Method:** POST
  - **URL:** `/api/events/{event_id}/attendance`
  - **Request:** `{ "student_id": 123 }`
  - **Response:** `{ "attendance_id": 456, "message": "Attendance marked" }`

- **Collect Feedback**
  - **Method:** POST
  - **URL:** `/api/events/{event_id}/feedback`
  - **Request:** `{ "student_id": 123, "rating": 4 }`
  - **Response:** `{ "feedback_id": 789, "message": "Feedback submitted" }`

- **Generate Reports**
  - **Method:** GET
  - **URL:** `/api/reports`
  - **Response:** `{ "total_registrations": 100, "attendance_percentage": 75, "average_feedback": 4.2, "event_popularity": [{"event_id": 1, "popularity": 90}], "student_participation": [{"student_id": 123, "events_attended": 5}], "top_active_students": [{"student_id": 123, "events_attended": 5}] }`

### 5. Workflows

- **Student Registration:**
  1. Student accesses the registration page on the mobile app.
  2. Student fills in personal details and submits the form.
  3. Backend processes the registration and returns a confirmation.

- **Event Check-in:**
  1. Student arrives at the event location.
  2. Student checks in via the mobile app.
  3. Backend records the attendance and confirms check-in.

### 6. Edge Cases

- **Duplicate Registrations:**
  - Ensure unique constraints on student-event registration to prevent duplicates.

- **Cancelled Events:**
  - Implement a status field in the Events table to handle cancellations and notify registered students.

- **Feedback Submission:**
  - Validate that feedback is only accepted from students who attended the event.

- **Concurrent Check-ins:**
  - Handle potential race conditions during high-volume check-ins by using transaction locks.

