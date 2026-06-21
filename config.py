import os

HF_TOKEN = os.getenv("HF_TOKEN")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
VECTOR_DB_DIR = "./chroma_db"
DEFAULT_RETRIEVAL_K = 3

PDF_SOURCES = [
    "data/company_policies.pdf",
]
MCP_DATA_FILE = "data/mcp_enterprise_updates.txt"

SAMPLE_QUERIES = [
    "What is the leave policy for full-time employees?",
    "How should employees report a security incident?",
    "What are the escalation steps for critical support tickets?",
]