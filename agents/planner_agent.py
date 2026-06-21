from crewai import Agent


def get_planner_agent():
    return Agent(
        role="Enterprise Query Planner",
        goal="Break user questions into evidence needs and route them to retrieval and MCP sources",
        backstory="Specialist in enterprise knowledge workflows and information planning",
        verbose=True,
    )
