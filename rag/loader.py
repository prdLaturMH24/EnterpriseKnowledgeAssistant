from langchain_community.document_loaders import PyPDFLoader


def load_documents(file_paths):
    documents = []
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    return documents