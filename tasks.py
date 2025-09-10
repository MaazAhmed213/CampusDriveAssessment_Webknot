from crewai import Task, Agent

def get_design_task(agent: Agent, requirements: str) -> Task:
    """
    Task for the System Architect to create the design document.
    """
    return Task(
        description=f"""
            Analyze the requirements for a Campus Event Management Platform and create a detailed design document in Markdown format.
            The document must be comprehensive and cover all aspects mentioned in the requirements.

            **Requirements:**
            ---
            {requirements}
            ---

            **Design Document Sections to Include:**
            1.  **Assumptions & Decisions:** Note down any assumptions made.
            2.  **Data to Track:** Detail data points for event creation, student registration, attendance, and feedback.
            3.  **Database Schema:** Provide a schema for tables like Colleges, Students, Events, Registrations. Address data separation and unique ID considerations.
            4.  **API Design:** Define RESTful API endpoints (Method, URL, Request, Response) for all required functionalities like student registration, attendance, feedback, and report generation.
            5.  **Workflows:** Briefly describe the sequence for key processes like student registration and event check-in.
            6.  **Edge Cases:** Mention potential edge cases like duplicate registrations or cancelled events.
        """,
        expected_output="A single, comprehensive Markdown file named 'DESIGN.md' that contains the complete design document as specified.",
        agent=agent,
        output_file="DESIGN.md"
    )

def get_schema_task(agent: Agent, context_tasks: list) -> Task:
    """
    Task for the DBA to create the SQL schema from the design document.
    """
    return Task(
        description="""
            Based on the 'Database Schema' section of the 'DESIGN.md' file, write a complete SQL script for SQLite.
            The script should be clean, well-formatted, and ready to be executed to set up the database, including primary and foreign keys.
        """,
        expected_output="A single SQL file named 'schema.sql' containing ONLY the raw SQL `CREATE TABLE` statements. There should be NO other text, explanations, or markdown formatting like ```sql.",
        agent=agent,
        context=context_tasks,
        output_file="schema.sql"
    )

def get_api_task(agent: Agent, context_tasks: list) -> Task:
    """
    Task for the Backend Developer to write the Flask API code.
    """
    return Task(
        description="""
            Implement a working backend prototype in a single Python file using Flask and the `sqlite3` module, based on the 'DESIGN.md' and 'schema.sql' files.

            **Implementation Details:**
            1.  Use Flask to create the web server.
            2.  **CRITICAL:** You must implement CORS (Cross-Origin Resource Sharing) to allow the Streamlit frontend (running on a different port) to communicate with this API. Import `CORS` from the `flask_cors` library and initialize it on your Flask app instance like this: `CORS(app)`.
            3.  Use the `sqlite3` library to interact with a database file named `campus_events.db`.
            4.  Implement all API endpoints as defined in the 'API Design' section of 'DESIGN.md' for student registration, attendance, feedback, and reporting.
            5.  Include a function to initialize the database using 'schema.sql'.
            6.  Ensure the complete, runnable code is in a single, well-commented file.
        """,
        expected_output="A single Python file named 'main.py' containing the complete Flask application with all specified API endpoints and database logic, including the necessary CORS configuration.",
        agent=agent,
        context=context_tasks,
        output_file="main.py"
    )

def get_readme_task(agent: Agent, context_tasks: list) -> Task:
    """
    Task for the Technical Writer to create the README file.
    """
    return Task(
        description="""
            Create a comprehensive `README.md` file for the generated Campus Event Management System prototype.

            **README Sections to Include:**
            1.  **Project Title & Overview:** A summary based on the assignment.
            2.  **Features:** A bulleted list of the implemented API features.
            3.  **Setup and Installation:** Step-by-step instructions (prerequisites, virtual environment, dependencies, database initialization).
            4.  **Running the Application:** Explain how to start the Flask server and the Streamlit UI.
            5.  **IMPORTANT - PERSONAL UNDERSTANDING SECTION:**
                - Create a section titled 'My Personal Understanding of the Project'.
                - Add a prominent placeholder text warning the user that this section must be filled out manually, as per the assignment rules.
        """,
        expected_output="A complete `README.md` file with all the specified sections, including the critical placeholder for the user's personal input.",
        agent=agent,
        context=context_tasks,
        output_file="README.md"
    )

def get_ui_task(agent: Agent, context_tasks: list) -> Task:
    """
    Task for the Frontend Developer to create the Streamlit UI.
    """
    return Task(
        description="""
            Based on the 'main.py' Flask application, create a user-friendly Streamlit application in a single file named `streamlit_app.py`.

            **UI Requirements:**
            1.  **Title:** Give the app a clear title like "Campus Event Management Portal".
            2.  **Separate Sections:** Use tabs or expanders for different functionalities (e.g., "Register Student", "Mark Attendance", "View Reports").
            3.  **API Interaction:**
                - Use the `requests` library to make calls to the Flask API endpoints defined in `main.py`.
                - Assume the Flask app is running locally at `http://127.0.0.1:5000`.
                - Create forms with `st.form` for user inputs (e.g., student ID, event ID).
            4.  **Display Data:**
                - For report endpoints, fetch the data and display it neatly using Streamlit components like `st.dataframe` or `st.markdown`.
            5.  **Error Handling:** Show user-friendly success or error messages using `st.success` or `st.error`.
            6.  **Completeness:** The script must be a complete, runnable Streamlit application.
        """,
        expected_output="A single Python file named 'streamlit_app.py' containing the complete Streamlit application.",
        agent=agent,
        context=context_tasks,
        output_file="streamlit_app.py"
    )

