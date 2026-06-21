from config import DEFAULT_RETRIEVAL_K


def get_retriever(vector_db):
    return vector_db.as_retriever(search_kwargs={"k": DEFAULT_RETRIEVAL_K})