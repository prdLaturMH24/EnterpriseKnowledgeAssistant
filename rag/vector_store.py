from langchain_community.vectorstores import Chroma
from config import VECTOR_DB_DIR

def create_vector_store(chunks, embedding):
    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=VECTOR_DB_DIR
    )