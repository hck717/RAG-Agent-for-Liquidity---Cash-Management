import os
import sqlite3
import pandas as pd
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
import shutil

# --- Configuration ---
DB_PATH = "financial_data.db"
VECTOR_DB_PATH = "chroma_db"
DOCS_PATH = "docs/knowledge_base"

# --- 1. Setup SQLite Database (Mock Data) ---
def setup_sql_db():
    print(f"Setting up SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Accounts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            company_name TEXT,
            currency TEXT,
            balance REAL,
            region TEXT
        )
    ''')

    # Create Transactions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            account_id TEXT,
            amount REAL,
            currency TEXT,
            date TEXT,
            description TEXT,
            FOREIGN KEY (account_id) REFERENCES accounts (account_id)
        )
    ''')

    # Insert Mock Data
    # Scenario: User has 4M USD, wants to send 5M USD.
    accounts_data = [
        ('ACC001', 'Global Tech HK Ltd', 'USD', 4000000.00, 'Hong Kong'),
        ('ACC002', 'Global Tech Brazil', 'BRL', 15000000.00, 'Brazil'),
        ('ACC003', 'Global Tech HK Ltd', 'HKD', 80000000.00, 'Hong Kong')
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?)', accounts_data)
    
    conn.commit()
    conn.close()
    print("SQLite database setup complete.")

# --- 2. Setup Vector Database (RAG) ---
def setup_vector_db():
    print(f"Setting up Vector database at {VECTOR_DB_PATH}...")
    
    # Load Documents
    if not os.path.exists(DOCS_PATH):
        os.makedirs(DOCS_PATH)
        print(f"Created directory {DOCS_PATH}. Please add documents there.")
        return

    loader = DirectoryLoader(DOCS_PATH, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("No documents found to ingest.")
        return

    # Split Text
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Embed and Store
    try:
        # Determine Embedding Model
        if os.environ.get("OPENAI_API_KEY"):
            print("Using OpenAI Embeddings...")
            embedding_function = OpenAIEmbeddings()
        else:
            print("OPENAI_API_KEY not found. Using Local Embeddings (HuggingFace)...")
            # Using a small, fast local model suitable for CPU
            embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Clear old DB if exists to avoid duplicates/conflicts
        if os.path.exists(VECTOR_DB_PATH):
            shutil.rmtree(VECTOR_DB_PATH)
            
        db = Chroma.from_documents(docs, embedding_function, persist_directory=VECTOR_DB_PATH)
        db.persist()
        print("Vector database setup complete.")
    except Exception as e:
        print(f"Failed to create Vector DB: {e}")

if __name__ == "__main__":
    setup_sql_db()
    setup_vector_db()
