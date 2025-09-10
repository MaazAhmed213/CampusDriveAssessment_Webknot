from crewai import Crew, Process

def get_crew(agents, tasks):
    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True

    )
