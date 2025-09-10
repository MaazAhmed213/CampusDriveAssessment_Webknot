import streamlit as st
import requests

# Base URL for API
BASE_URL = "http://127.0.0.1:5000/api"

st.title("Campus Event Management Portal")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Register Student",
    "Create Event",
    "Register for Event",
    "Mark Attendance",
    "View Reports"
])

# -----------------------
# Register Student
# -----------------------
with tab1:
    st.header("Register Student")
    with st.form("register_student_form"):
        name = st.text_input("Student Name")
        email = st.text_input("Student Email")
        college_id = st.number_input("College ID", min_value=1, step=1)
        submitted = st.form_submit_button("Register")
        if submitted:
            response = requests.post(f"{BASE_URL}/students/register", json={
                "name": name,
                "email": email,
                "college_id": college_id
            })
            if response.status_code == 200:
                st.success("Student registered successfully!")
            else:
                st.error("Failed to register student.")

# -----------------------
# Create Event
# -----------------------
with tab2:
    st.header("Create Event")
    with st.form("create_event_form"):
        name = st.text_input("Event Name")
        description = st.text_area("Description")
        date = st.date_input("Event Date")
        time = st.time_input("Event Time")
        location = st.text_input("Location")
        submitted = st.form_submit_button("Create Event")
        if submitted:
            payload = {
                "name": name,
                "description": description,
                "date": str(date),
                "time": str(time),
                "location": location,
                "created_by": 1
            }
            response = requests.post(f"{BASE_URL}/events/create", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Event created successfully! Event ID: {result['event_id']}")
            else:
                st.error("Failed to create event.")

# -----------------------
# Register for Event
# -----------------------
with tab3:
    st.header("Register for Event")
    with st.form("register_event_form"):
        student_id = st.number_input("Student ID", min_value=1, step=1)
        event_id = st.number_input("Event ID", min_value=1, step=1)
        submitted = st.form_submit_button("Register for Event")
        if submitted:
            response = requests.post(f"{BASE_URL}/events/{event_id}/register", json={
                "student_id": student_id
            })
            if response.status_code == 200:
                st.success("Student registered for event successfully!")
            else:
                st.error("Failed to register student for event.")

# -----------------------
# Mark Attendance
# -----------------------
with tab4:
    st.header("Mark Attendance")
    with st.form("mark_attendance_form"):
        student_id = st.number_input("Student ID (for attendance)", min_value=1, step=1)
        event_id = st.number_input("Event ID (for attendance)", min_value=1, step=1)
        submitted = st.form_submit_button("Mark Attendance")
        if submitted:
            response = requests.post(f"{BASE_URL}/events/{event_id}/attendance", json={
                "student_id": student_id
            })
            if response.status_code == 200:
                st.success("Attendance marked successfully!")
            else:
                st.error("Failed to mark attendance.")

# -----------------------
# View Reports
# -----------------------
with tab5:
    st.header("View Reports")
    if st.button("Generate Reports"):
        response = requests.get(f"{BASE_URL}/reports")
        if response.status_code == 200:
            data = response.json()

            st.markdown(f"**Total Registrations:** {data['total_registrations']}")
            st.markdown(f"**Attended Registrations:** {data['attended_registrations']}")
            st.markdown(f"**Attendance Percentage:** {data['attendance_percentage']:.2f}%")

            if not data["feedback_available"]:
                st.markdown("**Average Feedback Rating:** No feedback yet")
            else:
                st.markdown(f"**Average Feedback Rating:** {data['average_feedback']:.2f}")

            st.subheader("📈 Event Popularity (by registrations)")
            if data['event_popularity']:
                st.dataframe(data['event_popularity'])
            else:
                st.write("No event popularity data available.")

            st.subheader("👥 Student Participation (events attended)")
            if data['student_participation']:
                st.dataframe(data['student_participation'])
            else:
                st.write("No student participation data available.")

            st.subheader("🏆 Top Active Students")
            if data['top_active_students']:
                st.dataframe(data['top_active_students'])
            else:
                st.write("No student participation data available.")
        else:
            st.error("Failed to fetch reports.")

# import streamlit as st
# import requests

# # Set the base URL for the Flask API
# BASE_URL = "http://127.0.0.1:5000/api"

# # Title of the Streamlit app
# st.title("Campus Event Management Portal")

# # Create tabs
# tab1, tab2, tab3, tab4 = st.tabs([
#     "Register Student",
#     "Register for Event",
#     "Mark Attendance",
#     "View Reports"
# ])

# # -----------------------
# # Register Student
# # -----------------------
# with tab1:
#     st.header("Register Student")
#     with st.form("register_student_form"):
#         name = st.text_input("Student Name")
#         email = st.text_input("Student Email")
#         college_id = st.number_input("College ID", min_value=1, step=1)
#         submitted = st.form_submit_button("Register")
        
#         if submitted:
#             response = requests.post(f"{BASE_URL}/students/register", json={
#                 "name": name,
#                 "email": email,
#                 "college_id": college_id
#             })
#             if response.status_code == 200:
#                 st.success("Student registered successfully!")
#             else:
#                 st.error("Failed to register student.")

# # -----------------------
# # Register for Event
# # -----------------------
# with tab2:
#     st.header("Register for Event")
#     with st.form("register_event_form"):
#         student_id = st.number_input("Student ID", min_value=1, step=1)
#         event_id = st.number_input("Event ID", min_value=1, step=1)
#         submitted = st.form_submit_button("Register for Event")

#         if submitted:
#             response = requests.post(f"{BASE_URL}/events/{event_id}/register", json={
#                 "student_id": student_id
#             })
#             if response.status_code == 200:
#                 st.success("Student registered for event successfully!")
#             else:
#                 st.error("Failed to register student for event.")

# # -----------------------
# # Mark Attendance
# # -----------------------
# with tab3:
#     st.header("Mark Attendance")
#     with st.form("mark_attendance_form"):
#         student_id = st.number_input("Student ID (for attendance)", min_value=1, step=1)
#         event_id = st.number_input("Event ID (for attendance)", min_value=1, step=1)
#         submitted = st.form_submit_button("Mark Attendance")
        
#         if submitted:
#             response = requests.post(f"{BASE_URL}/events/{event_id}/attendance", json={
#                 "student_id": student_id
#             })
#             if response.status_code == 200:
#                 st.success("Attendance marked successfully!")
#             else:
#                 st.error("Failed to mark attendance.")

# # -----------------------
# # View Reports
# # -----------------------
# with tab4:
#     st.header("View Reports")
#     if st.button("Generate Reports"):
#         response = requests.get(f"{BASE_URL}/reports")
#         if response.status_code == 200:
#             data = response.json()

#             st.markdown(f"**Total Registrations:** {data['total_registrations']}")
#             st.markdown(f"**Attended Registrations:** {data['attended_registrations']}")
#             st.markdown(f"**Attendance Percentage:** {data['attendance_percentage']:.2f}%")

#             if not data["feedback_available"]:
#                 st.markdown("**Average Feedback Rating:** No feedback yet")
#             else:
#                 st.markdown(f"**Average Feedback Rating:** {data['average_feedback']:.2f}")

#             st.subheader("📈 Event Popularity (by registrations)")
#             if data['event_popularity']:
#                 st.dataframe(data['event_popularity'])
#             else:
#                 st.write("No event popularity data available.")

#             st.subheader("👥 Student Participation (events attended)")
#             if data['student_participation']:
#                 st.dataframe(data['student_participation'])
#             else:
#                 st.write("No student participation data available.")

#             st.subheader("🏆 Top Active Students")
#             if data['top_active_students']:
#                 st.dataframe(data['top_active_students'])
#             else:
#                 st.write("No student participation data available.")
#         else:
#             st.error("Failed to fetch reports.")

