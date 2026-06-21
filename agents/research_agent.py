from crewai import Agent

def get_research_agent():
    return Agent(
        role="Research Specialist",
        goal="Retrieve relevant context from knowledge base",
        backstory="Expert in enterprise search and document retrieval",
        verbose=True
    )