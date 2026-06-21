from rag.loader import load_documents
from rag.splitter import split_docs
from rag.embeddings import get_embeddings
from rag.vector_store import create_vector_store
from rag.retriever import get_retriever

from agents.research_agent import get_research_agent
from agents.response_agent import get_response_agent
from agents.evaluation_agent import get_evaluation_agent
from agents.mcp_agent import get_mcp_agent

from evaluation.ragas_eval import evaluate_response

from crewai import Crew, Task

# Step 1: Load and prepare RAG
docs = load_documents("data/company_policies.pdf.pdf")
chunks = split_docs(docs)
embeddings = get_embeddings()
vector_db = create_vector_store(chunks, embeddings)
retriever = get_retriever(vector_db)

# Step 2: Input Query
user_query = input("Enter your query: ")

# Step 3: Retrieve Context
retrieved_docs = retriever.get_relevant_documents(user_query)
context = [doc.page_content for doc in retrieved_docs]

print("\n--- Retrieved Context ---\n")
for doc in context:
    print(doc[:200], "\n")

# Step 4: MCP File Read (Example)
# file_data = read_file("data/sample.txt")
# print("\n--- MCP File Data ---\n", file_data)

# Step 5: Create Agents
research_agent = get_research_agent()
response_agent = get_response_agent()
evaluation_agent = get_evaluation_agent()
mcp_agent = get_mcp_agent()

# Step 6: Define Tasks
task_research = Task(
    description=f"Analyze the query: {user_query} and context: {context}",
    agent=research_agent
)

task_response = Task(
    description=f"Generate answer for query: {user_query} using context",
    agent=response_agent
)

task_mcp = Task(
    description="Fetch additional enterprise data using MCP",
    agent=mcp_agent
)

task_eval = Task(
    description="Evaluate response quality",
    agent=evaluation_agent
)

# Step 7: Crew Execution
crew = Crew(
    agents=[research_agent, response_agent, evaluation_agent, mcp_agent],
    tasks=[task_research, task_response, task_mcp, task_eval],
    verbose=True
)

result = crew.kickoff()

# Step 8: Evaluate using RAGAS
generated_answer = str(result)

evaluation = evaluate_response(
    user_query,
    generated_answer,
    context
)

print("\n--- Final Answer ---\n", generated_answer)
print("\n--- RAGAS Evaluation ---\n", evaluation)