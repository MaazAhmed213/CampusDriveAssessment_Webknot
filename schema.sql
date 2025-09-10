CREATE TABLE Colleges (
    college_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    college_id INTEGER,
    FOREIGN KEY (college_id) REFERENCES Colleges(college_id)
);

CREATE TABLE Events (
    event_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    location TEXT NOT NULL,
    created_by INTEGER NOT NULL
);

CREATE TABLE Registrations (
    registration_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    event_id INTEGER,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

CREATE TABLE Attendance (
    attendance_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    event_id INTEGER,
    check_in_timestamp TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

CREATE TABLE Feedback (
    feedback_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    event_id INTEGER,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    timestamp TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);
