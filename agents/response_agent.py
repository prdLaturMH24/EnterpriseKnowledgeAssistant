from crewai import Agent


def get_response_agent():
    return Agent(
        role="Response Generator",
        goal="Generate an accurate final response grounded in RAG evidence and MCP enterprise updates",
        backstory="Expert in enterprise policy communication and actionable answer writing",
        verbose=True,
    )