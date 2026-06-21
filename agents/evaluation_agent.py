from crewai import Agent

def get_evaluation_agent():
    return Agent(
        role="Evaluation Specialist",
        goal="Evaluate answer quality using RAGAS metrics",
        backstory="Expert in AI evaluation",
        verbose=True
    )