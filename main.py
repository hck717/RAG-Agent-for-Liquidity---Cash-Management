import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# --- Configuration ---
DB_PATH = "financial_data.db"
VECTOR_DB_PATH = "chroma_db"

st.set_page_config(page_title="Liquidity & Cash Management Agent", layout="wide")

# --- Tools ---

@tool
def get_account_balance(currency: str):
    """Query the SQL database to find the account balance for a specific currency."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT account_id, balance, currency FROM accounts WHERE currency = ?", (currency,))
    result = cursor.fetchall()
    conn.close()
    
    if not result:
        return f"No account found for currency {currency}."
    
    # Formatting result
    response = ""
    for row in result:
        response += f"Account ID: {row[0]}, Balance: {row[1]:,.2f} {row[2]}\n"
    return response

@tool
def check_compliance_rules(query: str):
    """Search the knowledge base (RAG) for compliance guidelines, specifically for FX and cross-border transfers."""
    if not os.path.exists(VECTOR_DB_PATH):
        return "Knowledge base not initialized."
    
    try:
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embedding_function)
        retriever = db.as_retriever()
        docs = retriever.invoke(query)
        
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error querying knowledge base: {str(e)}"

@tool
def run_stress_test(rate_drop_percent: float, receivables_delay_days: int):
    """
    Run a liquidity stress test simulation.
    Args:
        rate_drop_percent: The percentage drop in interest rate (e.g., 2.0 for 2%).
        receivables_delay_days: The number of days sales are delayed (e.g., 30).
    """
    # Mock Simulation Logic
    # Baseline Cash Flow (Simplified)
    days = range(1, 31)
    baseline_cash = [5000000 - (i * 100000) for i in days] # Burn rate
    
    # Stressed Cash Flow
    # Effect 1: Rate drop reduces interest income (minor impact for this short term, but we simulate it)
    # Effect 2: Receivables delay means a big inflow chunk is pushed out
    
    stressed_cash = []
    current_balance = 5000000 # Starting HKD balance (simplified)
    
    payroll_day = 15
    payroll_amount = 2000000
    
    inflow_day = 10
    inflow_amount = 3000000 # Expected receivable
    
    for day in days:
        daily_burn = 100000
        
        # Apply Inflow (delayed if stress)
        actual_inflow_day = inflow_day + receivables_delay_days
        if day == actual_inflow_day:
            current_balance += inflow_amount
        elif day == inflow_day and receivables_delay_days == 0:
             current_balance += inflow_amount
             
        # Apply Outflow (Payroll)
        if day == payroll_day:
            current_balance -= payroll_amount
            
        current_balance -= daily_burn
        stressed_cash.append(current_balance)
        
    # Analyze Result
    min_balance = min(stressed_cash)
    negative_days = [d for d, b in zip(days, stressed_cash) if b < 0]
    
    result_msg = f"Stress Test Results (Rate -{rate_drop_percent}%, Delay {receivables_delay_days} days):\n"
    if min_balance < 0:
        result_msg += f"CRITICAL: Liquidity shortage detected. Minimum balance hits {min_balance:,.2f} on Day {negative_days[0]}.\n"
        result_msg += f"You will need to draw down from your revolver facility to cover payroll on Day {payroll_day}."
    else:
        result_msg += f"Status OK. Minimum balance is {min_balance:,.2f}. Liquidity remains positive."
        
    return result_msg

# --- Agent Setup ---
def get_agent():
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [get_account_balance, check_compliance_rules, run_stress_test]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful Corporate Treasury AI Assistant. "
                   "You verify account balances using SQL tools. "
                   "You check compliance regulations using RAG tools. "
                   "You can run stress tests simulations."
                   "Always cite your source (e.g., 'According to the database...', 'Based on the compliance guidelines...')."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

# --- UI Layout ---
st.title("💰 Corporate Treasury AI Agent")
st.markdown("POC: Liquidity Management & Compliance Checker")

# Sidebar for Config
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.markdown("---")
    if st.button("Initialize System (Reset DBs)"):
        with st.spinner("Initializing databases..."):
            os.system("python initialize_system.py")
            st.success("System Initialized!")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about cash, compliance, or stress tests..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not os.environ.get("OPENAI_API_KEY"):
            st.error("Please enter your OpenAI API Key in the sidebar.")
        else:
            agent = get_agent()
            with st.spinner("Agent is thinking..."):
                try:
                    response = agent.invoke({"input": prompt})
                    st.markdown(response["output"])
                    st.session_state.messages.append({"role": "assistant", "content": response["output"]})
                except Exception as e:
                    st.error(f"Error: {e}")
