import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

VECTOR_DB_PATH = "chroma_db"

def execute_rag_check(query: str) -> str:
    """
    Queries the Chroma vector database for relevant compliance documents.
    """
    if not os.path.exists(VECTOR_DB_PATH):
        return "Knowledge base not initialized."
    
    try:
        # Detect Embedding Model based on Environment
        if os.environ.get("OPENAI_API_KEY"):
            embedding_function = OpenAIEmbeddings()
        else:
            embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
        db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embedding_function)
        retriever = db.as_retriever()
        docs = retriever.invoke(query)
        
        if not docs:
            return "No relevant compliance rules found."
        
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error querying knowledge base: {str(e)}"
