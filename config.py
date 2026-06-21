import os

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
VECTOR_DB_DIR = "./chroma_db"