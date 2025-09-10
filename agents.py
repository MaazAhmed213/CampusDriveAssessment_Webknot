from crewai import Agent
from langchain_openai import ChatOpenAI

def get_architect_agent(llm: ChatOpenAI) -> Agent:
    """
    Creates the System Architect agent responsible for creating the initial design document.
    """
    return Agent(
        role="Senior System Architect",
        goal="Create a comprehensive design document for the Campus Event Management Platform's reporting system based on the provided requirements.",
        backstory=(
            "An experienced system architect who specializes in breaking down complex requirements "
            "into clear, actionable design documents, including database schemas, API endpoints, "
            "and system workflows. You always consider scalability and edge cases."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

def get_db_admin_agent(llm: ChatOpenAI) -> Agent:
    """
    Creates the Database Administrator agent responsible for writing the SQL schema.
    """
    return Agent(
        role="Database Administrator",
        goal="Generate a SQL script to create the database schema based on the design document provided.",
        backstory=(
            "A meticulous Database Administrator skilled in translating ER diagrams and schema designs "
            "into efficient and well-structured SQL code, specifically for SQLite."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

def get_backend_dev_agent(llm: ChatOpenAI) -> Agent:
    """
    Creates the Backend Developer agent responsible for implementing the API prototype.
    """
    return Agent(
        role="Python Backend Developer",
        goal="Implement the backend logic and APIs for the event management system using Python, Flask, and SQLite based on the design document and database schema.",
        backstory=(
            "A proficient Python developer with expertise in building robust and scalable RESTful APIs "
            "using Flask. They follow best practices to create clean, documented, and maintainable code."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

def get_tech_writer_agent(llm: ChatOpenAI) -> Agent:
    """
    Creates the Technical Writer agent responsible for generating the README file.
    """
    return Agent(
        role="Technical Writer",
        goal="Create a clear and concise README.md file that explains how to set up and run the generated prototype.",
        backstory=(
            "A professional technical writer who excels at creating user-friendly documentation for software projects. "
            "They ensure that setup and usage instructions are easy to follow for any developer."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

def get_frontend_dev_agent(llm: ChatOpenAI) -> Agent:
    """
    Creates the Frontend Developer agent for building the Streamlit UI.
    """
    return Agent(
        role="Streamlit Frontend Developer",
        goal="Create an intuitive and functional Streamlit web application to interact with the backend APIs.",
        backstory=(
            "A creative and skilled frontend developer who excels at building data-driven web applications "
            "with Streamlit. They can quickly prototype and build user-friendly interfaces that "
            "effectively communicate with backend services."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
