from crewai import Crew, Task

from agents.evaluation_agent import get_evaluation_agent
from agents.mcp_agent import get_mcp_agent
from agents.planner_agent import get_planner_agent
from agents.research_agent import get_research_agent
from agents.response_agent import get_response_agent
from config import MCP_DATA_FILE, PDF_SOURCES, SAMPLE_QUERIES
from evaluation.ragas_eval import evaluate_response
from mcp.filesystem_server import read_enterprise_updates
from rag.embeddings import get_embeddings
from rag.loader import load_documents
from rag.retriever import get_retriever
from rag.splitter import split_docs
from rag.vector_store import create_vector_store


def build_rag_pipeline():
    docs = load_documents(PDF_SOURCES)
    chunks = split_docs(docs)
    embeddings = get_embeddings()
    vector_db = create_vector_store(chunks, embeddings)
    retriever = get_retriever(vector_db)
    return retriever


def format_context(retrieved_docs):
    context_lines = []
    for idx, doc in enumerate(retrieved_docs, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "NA")
        snippet = doc.page_content.strip().replace("\n", " ")
        context_lines.append(f"[RAG-{idx}] source={source}, page={page}: {snippet}")
    return context_lines


def run_query(retriever, user_query):
    print("\n=== Pipeline: query → retrieval → agent collaboration → MCP enrichment → response → RAGAS ===")
    print(f"\nUser Query: {user_query}\n")

    retrieved_docs = retriever.invoke(user_query)
    context_lines = format_context(retrieved_docs)

    print("--- Retrieved Context (RAG) ---")
    for line in context_lines:
        print(f"- {line[:260]}")

    mcp_data = read_enterprise_updates(MCP_DATA_FILE, user_query)
    print("\n--- MCP Supplemental Data ---")
    print(mcp_data[:800])

    planner_agent = get_planner_agent()
    research_agent = get_research_agent()
    mcp_agent = get_mcp_agent()
    response_agent = get_response_agent()
    evaluation_agent = get_evaluation_agent()

    task_plan = Task(
        description=(
            f"Break down this enterprise query into evidence needs and answer goals: {user_query}. "
            "Return concise bullet points."
        ),
        expected_output="A short evidence plan listing what must be validated from RAG and MCP data.",
        agent=planner_agent,
    )

    task_research = Task(
        description=(
            f"Using this retrieved context, extract only relevant evidence for the query.\n"
            f"Query: {user_query}\nContext:\n" + "\n".join(context_lines)
        ),
        expected_output="A concise evidence summary with references to the [RAG-x] entries used.",
        agent=research_agent,
        context=[task_plan],
    )

    task_mcp = Task(
        description=(
            f"Analyze this MCP filesystem data and extract enterprise updates related to the query.\n"
            f"Query: {user_query}\nMCP Data:\n{mcp_data}"
        ),
        expected_output="Relevant supplemental facts from MCP data.",
        agent=mcp_agent,
        context=[task_plan],
    )

    task_response = Task(
        description=(
            f"Generate the final answer for the user query.\n"
            f"Query: {user_query}\n"
            "Use the research evidence and MCP supplemental data, and cite evidence tags where applicable."
        ),
        expected_output="Final user-facing answer grounded in provided evidence.",
        agent=response_agent,
        context=[task_research, task_mcp],
    )

    task_eval_summary = Task(
        description=(
            "Review the generated answer and provide a short qualitative quality note before metric scoring."
        ),
        expected_output="A short quality observation statement.",
        agent=evaluation_agent,
        context=[task_response],
    )

    crew = Crew(
        agents=[planner_agent, research_agent, mcp_agent, response_agent, evaluation_agent],
        tasks=[task_plan, task_research, task_mcp, task_response, task_eval_summary],
        verbose=True,
    )

    crew_result = crew.kickoff()
    generated_answer = str(task_response.output) if task_response.output else str(crew_result)

    metric_scores = evaluate_response(
        user_query=user_query,
        generated_answer=generated_answer,
        context=context_lines,
    )

    print("\n--- Final Answer ---")
    print(generated_answer)
    print("\n--- RAGAS Evaluation ---")
    for metric in ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]:
        print(f"{metric}: {metric_scores[metric]:.4f}")
    print(f"interpretation: {metric_scores['interpretation']}")

    return {
        "query": user_query,
        "answer": generated_answer,
        "rag_context": context_lines,
        "mcp_data": mcp_data,
        "evaluation": metric_scores,
    }


def choose_queries():
    print("Choose mode:")
    print("1. Run single custom query")
    print("2. Run sample demo queries")
    mode = input("Enter option (1/2): ").strip()

    if mode == "2":
        return SAMPLE_QUERIES

    return [input("Enter your query: ").strip()]


def main():
    retriever = build_rag_pipeline()
    queries = choose_queries()
    results = []

    for query in queries:
        if not query:
            continue
        results.append(run_query(retriever, query))

    print("\n=== Execution Summary ===")
    print(f"Total queries processed: {len(results)}")


if __name__ == "__main__":
    main()
