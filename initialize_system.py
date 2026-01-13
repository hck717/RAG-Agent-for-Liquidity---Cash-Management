import os
import sqlite3
import pandas as pd
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
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
    
    # Check if API Key is set (User will need to set this in .env)
    if not os.environ.get("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not found in environment variables. Vector DB generation might fail if not using local embeddings.")
        # In a real scenario, we might default to a local embedding model like HuggingFace if no key is present.
        # For this POC, we assume the user will provide it or we code a fallback if requested.
        pass

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
    # Note: This requires an OpenAI API Key. 
    # For a purely local setup, one would use OllamaEmbeddings or HuggingFaceEmbeddings.
    try:
        embedding_function = OpenAIEmbeddings()
        
        # Clear old DB if exists to avoid duplicates in this POC script
        if os.path.exists(VECTOR_DB_PATH):
            shutil.rmtree(VECTOR_DB_PATH)
            
        db = Chroma.from_documents(docs, embedding_function, persist_directory=VECTOR_DB_PATH)
        db.persist()
        print("Vector database setup complete.")
    except Exception as e:
        print(f"Failed to create Vector DB: {e}")
        print("Ensure OPENAI_API_KEY is set or modify the script to use local embeddings.")

if __name__ == "__main__":
    setup_sql_db()
    setup_vector_db()
