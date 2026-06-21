from crewai import Agent


def get_research_agent():
    return Agent(
        role="Research Specialist",
        goal="Identify and summarize the most relevant evidence from retrieved enterprise knowledge chunks",
        backstory="Expert in enterprise search, evidence ranking, and context traceability",
        verbose=True,
    )