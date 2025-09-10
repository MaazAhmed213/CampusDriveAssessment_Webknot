import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai import Crew, Process

# Import agents and tasks
from agents import (
    get_architect_agent,
    get_db_admin_agent,
    get_backend_dev_agent,
    get_tech_writer_agent,
    get_frontend_dev_agent  # Import the new agent
)
from tasks import (
    get_design_task,
    get_schema_task,
    get_api_task,
    get_readme_task,
    get_ui_task  # Import the new task
)

load_dotenv()

def main():
    """
    Main function to orchestrate the CrewAI workflow for building the
    Campus Event Management System prototype, including a Streamlit UI.
    """
    print("## Welcome to the CrewAI-Powered Campus Event System Generator (OpenAI Edition)! ##")
    print("---------------------------------------------------------------------------------")

    # 1. Setup LLM with OpenAI
    try:
        llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.1,
        )
        print("OpenAI LLM Initialized successfully.")
    except Exception as e:
        print(f"Error initializing OpenAI Language Model: {e}")
        print("Please ensure your OPENAI_API_KEY is set correctly in the .env file.")
        return

    # 2. Define the Assignment Requirements
    assignment_requirements = """
    **Scenario:** Build a Campus Event Management Platform.
    **Core Components:** Admin Portal (Web) for staff, Student App (Mobile) for students.
    **Mission:** Design and implement a basic event reporting system.
    **Prototype Features:**
    - Database: SQLite
    - APIs: Register students, mark attendance, collect feedback (rating 1-5).
    - Reports: Total registrations, attendance percentage, average feedback, event popularity, student participation.
    - Bonus: Top 3 Active Students report.
    **Final Deliverables:** Design Document, DB Schema, Backend API, Streamlit UI, and a README.
    """

    # 3. Instantiate Agents
    architect = get_architect_agent(llm)
    db_admin = get_db_admin_agent(llm)
    backend_dev = get_backend_dev_agent(llm)
    tech_writer = get_tech_writer_agent(llm)
    frontend_dev = get_frontend_dev_agent(llm)  # Instantiate the new agent
    print("Agents created.")

    # 4. Instantiate Tasks
    design_task = get_design_task(architect, assignment_requirements)
    schema_task = get_schema_task(db_admin, [design_task])
    api_task = get_api_task(backend_dev, [design_task, schema_task])
    ui_task = get_ui_task(frontend_dev, [api_task])  # The UI task depends on the API task
    readme_task = get_readme_task(tech_writer, [api_task, ui_task]) # README now depends on API and UI
    print("Tasks created.")

    # 5. Form the Crew
    event_system_crew = Crew(
        agents=[architect, db_admin, backend_dev, frontend_dev, tech_writer], # Add frontend_dev before tech_writer
        tasks=[design_task, schema_task, api_task, ui_task, readme_task], # Add ui_task before readme_task
        process=Process.sequential,
        verbose=True  # FIX: Changed from 2 to True
    )
    print("Crew assembled. Kicking off the process...")
    print("----------------------------------------------------------------")

    # 6. Kickoff the Crew's work
    result = event_system_crew.kickoff()

    print("\n----------------------------------------------------------------")
    print("## CrewAI Process Finished! ##\n")
    print("Final Result:")
    print(result)
    print("\nGenerated files: DESIGN.md, schema.sql, main.py, streamlit_app.py, README.md")
    print("\n**IMPORTANT REMINDER:** Open `README.md` and fill in the 'My Personal Understanding of the Project' section.")
    
    print("\n\n================================================================================")
    print("====== DETAILED INSTRUCTIONS TO RUN THE GENERATED APPLICATION ======")
    print("================================================================================\n")
    print("You have successfully generated the project files. Follow these steps to run the application:\n")
    print("--- Step 1: Set up the Python Environment (if you haven't already) ---")
    print("1. **CRITICAL:** Make sure you have Python 3.11 or newer installed. This script will not work with older versions.")
    print("2. Open your terminal and check your Python 3.11 installation by running: `python3.11 --version`")
    print("   (Note: Your command might be `python` or `python3` if 3.11 is your default).")
    print("3. In the project directory, create a virtual environment using your Python 3.11 executable:")
    print("   `python3.11 -m venv venv`")
    print("4. Activate the virtual environment:")
    print("   - On Windows: `venv\\Scripts\\activate`")
    print("   - On macOS/Linux: `source venv/bin/activate`\n")
    
    print("--- Step 2: Install Required Libraries ---")
    print("1. Copy the following command EXACTLY and paste it into your activated terminal:")
    print("\n   pip install 'crewai[tools]' python-dotenv langchain-openai Flask streamlit requests\n")
    print("   (Note: Make sure to copy the entire line above, starting with 'pip' and nothing else.)\n")

    print("--- Step 3: Run the Backend API Server ---")
    print("1. Open a **NEW** terminal in the same project directory and activate the virtual environment (`source venv/bin/activate` or `venv\\Scripts\\activate`).")
    print("2. This terminal will be dedicated to the backend.")
    print("3. Run the Flask application:")
    print("   `python main.py`")
    print("4. You should see output indicating the server is running, something like `* Running on http://127.0.0.1:5000`\n")

    print("--- Step 4: Run the Streamlit Frontend Application ---")
    print("1. Open another **NEW** terminal (this is your second one) and activate the virtual environment again.")
    print("2. This terminal will be for the user interface.")
    print("3. Run the Streamlit application:")
    print("   `streamlit run streamlit_app.py`")
    print("4. Your app is now running locally, usually at `http://localhost:8501`.\n")

    print("--- Step 5 (Optional): Expose Your App with Ngrok ---")
    print("Ngrok creates a public URL for your local application so you can share it.")
    print("1. **Install Ngrok:** If you don't have it, install it. On macOS, you can use Homebrew: `brew install ngrok`.")
    print("   For other systems, download from https://ngrok.com/download")
    print("2. **Sign up and get your Authtoken:** Create a free account at https://ngrok.com/signup to get an authtoken.")
    print("3. **Configure Ngrok:** Connect your account using the token you just got:")
    print("   `ngrok config add-authtoken <YOUR_NGROK_AUTHTOKEN>`")
    print("4. **Expose Streamlit:** Open another **NEW** terminal (this is your third one). Expose the Streamlit app (which runs on port 8501) by running:")
    print("   `ngrok http 8501`")
    print("5. **Get your Public URL:** Ngrok will display a public URL in the terminal (e.g., `https://random-string.ngrok-free.app`). Anyone with this link can now access your Streamlit application!")
    print("\n================================================================================")


if __name__ == "__main__":
    main()

