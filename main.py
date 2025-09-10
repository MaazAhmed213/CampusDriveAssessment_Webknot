from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "campus_events.db"

def get_db_connection():
    conn = sqlite3.connect(
        DATABASE,
        check_same_thread=False,   # allow Flask threads to reuse connections
        timeout=10                 
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")  # enable write-ahead logging
    return conn


# ------------------------
# API Endpoints
# ------------------------

@app.route('/api/students/register', methods=['POST'])
def register_student():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    college_id = data.get("college_id")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Students (name, email, college_id) VALUES (?, ?, ?)",
        (name, email, college_id)
    )
    conn.commit()
    student_id = cur.lastrowid
    conn.close()

    return jsonify({"student_id": student_id, "message": "Registration successful"})


@app.route('/api/events/create', methods=['POST'])
def create_event():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")
    date = data.get("date")
    time = data.get("time")
    location = data.get("location")
    created_by = data.get("created_by", 1)  # default admin id

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Events (name, description, date, time, location, created_by) VALUES (?, ?, ?, ?, ?, ?)",
        (name, description, date, time, location, created_by)
    )
    conn.commit()
    event_id = cur.lastrowid
    conn.close()

    return jsonify({"event_id": event_id, "message": "Event created successfully"})


@app.route('/api/events/<int:event_id>/register', methods=['POST'])
def register_for_event(event_id):
    data = request.get_json()
    student_id = data.get("student_id")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Registrations (student_id, event_id, timestamp) VALUES (?, ?, datetime('now'))",
        (student_id, event_id)
    )
    conn.commit()
    registration_id = cur.lastrowid
    conn.close()

    return jsonify({"registration_id": registration_id, "message": "Event registration successful"})


@app.route('/api/events/<int:event_id>/attendance', methods=['POST'])
def mark_attendance(event_id):
    data = request.get_json()
    student_id = data.get("student_id")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Attendance (student_id, event_id, check_in_timestamp) VALUES (?, ?, datetime('now'))",
        (student_id, event_id)
    )
    conn.commit()
    attendance_id = cur.lastrowid
    conn.close()

    return jsonify({"attendance_id": attendance_id, "message": "Attendance marked"})


@app.route('/api/events/<int:event_id>/feedback', methods=['POST'])
def submit_feedback(event_id):
    data = request.get_json()
    student_id = data.get("student_id")
    rating = data.get("rating")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Feedback (student_id, event_id, rating, timestamp) VALUES (?, ?, ?, datetime('now'))",
        (student_id, event_id, rating)
    )
    conn.commit()
    feedback_id = cur.lastrowid
    conn.close()

    return jsonify({"feedback_id": feedback_id, "message": "Feedback submitted"})


@app.route('/api/reports', methods=['GET'])
def generate_reports():
    conn = get_db_connection()
    cur = conn.cursor()

    # Total registrations
    cur.execute("SELECT COUNT(*) FROM Registrations")
    total_registrations = cur.fetchone()[0]

    # Attended registrations
    cur.execute("""
        SELECT COUNT(DISTINCT r.registration_id)
        FROM Registrations r
        INNER JOIN Attendance a
        ON r.student_id = a.student_id AND r.event_id = a.event_id
    """)
    attended_registrations = cur.fetchone()[0]

    # Attendance %
    attendance_percentage = (attended_registrations / total_registrations * 100) if total_registrations > 0 else 0.0

    # Average feedback
    cur.execute("SELECT AVG(rating) FROM Feedback")
    avg = cur.fetchone()[0]
    if avg is None:
        average_feedback = None
        feedback_available = False
    else:
        average_feedback = float(avg)
        feedback_available = True

    # Event popularity
    cur.execute("""
        SELECT e.event_id, e.name, COUNT(r.registration_id) as registrations
        FROM Events e
        LEFT JOIN Registrations r ON e.event_id = r.event_id
        GROUP BY e.event_id
        ORDER BY registrations DESC
    """)
    event_popularity = [dict(row) for row in cur.fetchall()]

    # Top active students
    cur.execute("""
        SELECT s.student_id, s.name, COUNT(a.attendance_id) as events_attended
        FROM Students s
        LEFT JOIN Attendance a ON s.student_id = a.student_id
        GROUP BY s.student_id
        ORDER BY events_attended DESC
        LIMIT 5
    """)
    top_active_students = [dict(row) for row in cur.fetchall()]

    # Student participation
    cur.execute("""
        SELECT s.student_id, s.name, COUNT(DISTINCT a.event_id) as events_attended
        FROM Students s
        LEFT JOIN Attendance a ON s.student_id = a.student_id
        GROUP BY s.student_id
        ORDER BY events_attended DESC
    """)
    student_participation = [dict(row) for row in cur.fetchall()]

    conn.close()

    return jsonify({
        "total_registrations": total_registrations,
        "attended_registrations": attended_registrations,
        "attendance_percentage": attendance_percentage,
        "average_feedback": average_feedback,
        "feedback_available": feedback_available,
        "event_popularity": event_popularity,
        "top_active_students": top_active_students,
        "student_participation": student_participation
    })


if __name__ == "__main__":
    conn = get_db_connection()
    conn.close()
    app.run(debug=True)

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import sqlite3

# app = Flask(__name__)
# CORS(app)

# DATABASE = "campus_events.db"

# def get_db_connection():
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     return conn

# # ------------------------
# # API Endpoints
# # ------------------------

# @app.route('/api/students/register', methods=['POST'])
# def register_student():
#     data = request.get_json()
#     name = data.get("name")
#     email = data.get("email")
#     college_id = data.get("college_id")

#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO Students (name, email, college_id) VALUES (?, ?, ?)",
#         (name, email, college_id)
#     )
#     conn.commit()
#     student_id = cur.lastrowid
#     conn.close()

#     return jsonify({"student_id": student_id, "message": "Registration successful"})


# @app.route('/api/events/<int:event_id>/register', methods=['POST'])
# def register_for_event(event_id):
#     """Register a student for an event"""
#     data = request.get_json()
#     student_id = data.get("student_id")

#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO Registrations (student_id, event_id, timestamp) VALUES (?, ?, datetime('now'))",
#         (student_id, event_id)
#     )
#     conn.commit()
#     registration_id = cur.lastrowid
#     conn.close()

#     return jsonify({"registration_id": registration_id, "message": "Event registration successful"})


# @app.route('/api/events/<int:event_id>/attendance', methods=['POST'])
# def mark_attendance(event_id):
#     data = request.get_json()
#     student_id = data.get("student_id")

#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO Attendance (student_id, event_id, check_in_timestamp) VALUES (?, ?, datetime('now'))",
#         (student_id, event_id)
#     )
#     conn.commit()
#     attendance_id = cur.lastrowid
#     conn.close()

#     return jsonify({"attendance_id": attendance_id, "message": "Attendance marked"})


# @app.route('/api/events/<int:event_id>/feedback', methods=['POST'])
# def submit_feedback(event_id):
#     data = request.get_json()
#     student_id = data.get("student_id")
#     rating = data.get("rating")

#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO Feedback (student_id, event_id, rating, timestamp) VALUES (?, ?, ?, datetime('now'))",
#         (student_id, event_id, rating)
#     )
#     conn.commit()
#     feedback_id = cur.lastrowid
#     conn.close()

#     return jsonify({"feedback_id": feedback_id, "message": "Feedback submitted"})


# @app.route('/api/reports', methods=['GET'])
# def generate_reports():
#     conn = get_db_connection()
#     cur = conn.cursor()

#     # Total registrations (all student-event registrations)
#     cur.execute("SELECT COUNT(*) FROM Registrations")
#     total_registrations = cur.fetchone()[0]

#     # Students who actually attended (intersection of registrations & attendance)
#     cur.execute("""
#         SELECT COUNT(DISTINCT r.registration_id)
#         FROM Registrations r
#         INNER JOIN Attendance a
#         ON r.student_id = a.student_id AND r.event_id = a.event_id
#     """)
#     attended_registrations = cur.fetchone()[0]

#     # Attendance percentage
#     attendance_percentage = (attended_registrations / total_registrations * 100) if total_registrations > 0 else 0.0

#     # Average feedback
#     cur.execute("SELECT AVG(rating) FROM Feedback")
#     avg = cur.fetchone()[0]
#     if avg is None:
#         average_feedback = None
#         feedback_available = False
#     else:
#         average_feedback = float(avg)
#         feedback_available = True

#     # Event popularity (sorted by registrations)
#     cur.execute("""
#         SELECT e.event_id, e.name, COUNT(r.registration_id) as registrations
#         FROM Events e
#         LEFT JOIN Registrations r ON e.event_id = r.event_id
#         GROUP BY e.event_id
#         ORDER BY registrations DESC
#     """)
#     event_popularity = [dict(row) for row in cur.fetchall()]

#     # Top active students (by attendance count)
#     cur.execute("""
#         SELECT s.student_id, s.name, COUNT(a.attendance_id) as events_attended
#         FROM Students s
#         LEFT JOIN Attendance a ON s.student_id = a.student_id
#         GROUP BY s.student_id
#         ORDER BY events_attended DESC
#         LIMIT 5
#     """)
#     top_active_students = [dict(row) for row in cur.fetchall()]

#     # Student participation (all students with how many events they attended)
#     cur.execute("""
#         SELECT s.student_id, s.name, COUNT(DISTINCT a.event_id) as events_attended
#         FROM Students s
#         LEFT JOIN Attendance a ON s.student_id = a.student_id
#         GROUP BY s.student_id
#         ORDER BY events_attended DESC
#     """)
#     student_participation = [dict(row) for row in cur.fetchall()]

#     conn.close()

#     return jsonify({
#         "total_registrations": total_registrations,
#         "attended_registrations": attended_registrations,
#         "attendance_percentage": attendance_percentage,
#         "average_feedback": average_feedback,
#         "feedback_available": feedback_available,
#         "event_popularity": event_popularity,
#         "top_active_students": top_active_students,
#         "student_participation": student_participation
#     })


# if __name__ == "__main__":
#     conn = get_db_connection()
#     conn.close()
#     app.run(debug=True)
