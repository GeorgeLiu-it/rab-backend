from langchain_chroma import Chroma
from app.core.config import embeddings, COLLECTION_NAME

LOAD_PATH, VECTOR_DIR = "C:\\Users\\liushanshan\\Documents\\ai\\rag_ollama\\data", "C:\\Users\\liushanshan\\Documents\\ai\\rag_ollama\\vector_db"

def chroma_vector_store():
    """Chroma 向量数据库"""

    return Chroma(
        persist_directory=VECTOR_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )