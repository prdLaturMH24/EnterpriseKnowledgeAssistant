from crewai import Agent


def get_mcp_agent():
    return Agent(
        role="External System Connector",
        goal="Retrieve supplemental enterprise operational updates from MCP-integrated filesystem data",
        backstory="Expert in system integrations and enterprise source unification",
        verbose=True,
    )