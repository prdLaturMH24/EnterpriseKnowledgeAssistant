from crewai import Agent

def get_mcp_agent():
    return Agent(
        role="External System Connector",
        goal="Retrieve additional information from filesystem",
        backstory="Expert in system integrations",
        verbose=True
    )