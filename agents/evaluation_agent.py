from crewai import Agent


def get_evaluation_agent():
    return Agent(
        role="Evaluation Specialist",
        goal="Interpret RAGAS metrics and provide actionable quality feedback",
        backstory="Expert in LLM evaluation, metric interpretation, and quality risk detection",
        verbose=True,
    )