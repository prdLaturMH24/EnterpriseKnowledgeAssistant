from crewai import Agent

def get_response_agent():
    return Agent(
        role="Response Generator",
        goal="Generate accurate responses using retrieved context",
        backstory="Expert in business and technical communication",
        verbose=True
    )