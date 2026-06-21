from langchain_community.embeddings import HuggingFaceEmbeddings
from config import HF_TOKEN

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", huggingfacehub_api_token=HF_TOKEN)