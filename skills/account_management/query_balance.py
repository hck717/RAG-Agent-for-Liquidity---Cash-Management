import sqlite3
import os

DB_PATH = "financial_data.db"

def execute_query(currency: str) -> str:
    """
    Connects to the SQL database and retrieves the balance for the specified currency.
    """
    if not os.path.exists(DB_PATH):
        return f"Error: Database file '{DB_PATH}' not found. Please run initialize_system.py first."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT account_id, balance, currency FROM accounts WHERE currency = ?", (currency,))
        result = cursor.fetchall()
        
        if not result:
            return f"No account found for currency {currency}."
        
        response = ""
        for row in result:
            response += f"Account ID: {row[0]}, Balance: {row[1]:,.2f} {row[2]}\n"
        
        return response
    finally:
        conn.close()
