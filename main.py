import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# --- Configuration ---
DB_PATH = "financial_data.db"
VECTOR_DB_PATH = "chroma_db"
IMG_PATH = "stress_test_result.png"

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

@tool
def run_stress_test(rate_drop_percent: float, receivables_delay_days: int):
    """
    Run a liquidity stress test simulation and generate a forecast chart.
    Args:
        rate_drop_percent: The percentage drop in interest rate (e.g., 2.0 for 2%).
        receivables_delay_days: The number of days sales are delayed (e.g., 30).
    Returns:
        A string summary of the result. The function also saves a plot to 'stress_test_result.png'.
    """
    # Mock Simulation Logic
    days = list(range(1, 31))
    
    # Baseline: Starting 5M, burns 100k/day, Payroll 2M on Day 15, Inflow 3M on Day 10
    start_balance = 5000000
    daily_burn = 100000
    payroll_day = 15
    payroll_amount = 2000000
    base_inflow_day = 10
    inflow_amount = 3000000
    
    stressed_cash = []
    current_balance = start_balance
    
    for day in days:
        # 1. Inflow Logic
        actual_inflow_day = base_inflow_day + receivables_delay_days
        if day == actual_inflow_day:
            current_balance += inflow_amount
            
        # 2. Outflow Logic (Payroll)
        if day == payroll_day:
            current_balance -= payroll_amount
            
        # 3. Daily Burn
        current_balance -= daily_burn
        
        # 4. Interest Rate Impact (Simplified: Lower rate = less interest income, treated as extra cost for simplicity)
        # Assuming we earn 5% APY normally. Drop 2% means we earn less. 
        # For a cash agent POC, we might simulate 'cost of carry' increasing if we go negative.
        if current_balance < 0:
            overdraft_fee = abs(current_balance) * (0.10 / 365) # 10% penalty rate
            current_balance -= overdraft_fee
            
        stressed_cash.append(current_balance)
        
    # Generate Plot
    plt.figure(figsize=(10, 5))
    plt.plot(days, stressed_cash, marker='o', linestyle='-', color='b', label='Projected Balance')
    plt.axhline(y=0, color='r', linestyle='--', label='Zero Balance')
    plt.axvline(x=payroll_day, color='g', linestyle=':', label='Payroll Day')
    
    plt.title(f"Liquidity Stress Test (Rate -{rate_drop_percent}%, Delay {receivables_delay_days} days)")
    plt.xlabel("Day")
    plt.ylabel("Balance (HKD)")
    plt.legend()
    plt.grid(True)
    plt.savefig(IMG_PATH)
    plt.close()
    
    # Analyze Result
    min_balance = min(stressed_cash)
    negative_days = [d for d, b in zip(days, stressed_cash) if b < 0]
    
    result_msg = f"SIMULATION COMPLETE. Visual chart saved to {IMG_PATH}.\n"
    if min_balance < 0:
        result_msg += f"CRITICAL: Liquidity shortage detected. Minimum balance hits {min_balance:,.2f} on Day {negative_days[0]}.\n"
        result_msg += f"You will need to draw down from your revolver facility to cover payroll on Day {payroll_day}."
    else:
        result_msg += f"Status OK. Minimum balance is {min_balance:,.2f}. Liquidity remains positive."
        
    return result_msg

# --- Agent Setup ---
def get_agent(llm_choice, openai_api_key=None, local_model_name="llama3", local_base_url="http://localhost:11434"):
    tools = [get_account_balance, check_compliance_rules, run_stress_test]
    
    if llm_choice == "OpenAI":
        if not openai_api_key:
            raise ValueError("OpenAI API Key is required for OpenAI models.")
        llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=openai_api_key)
    else:
        # Local (Ollama)
        llm = ChatOllama(model=local_model_name, base_url=local_base_url, temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful Corporate Treasury AI Assistant. "
                   "You verify account balances using SQL tools. "
                   "You check compliance regulations using RAG tools. "
                   "You can run stress tests simulations using the 'run_stress_test' tool. "
                   "If you run a stress test, always mention that a chart has been generated."
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
    llm_provider = st.radio("LLM Provider", ["OpenAI", "Local (Ollama)"])
    
    api_key = ""
    local_model = "llama3"
    local_url = "http://localhost:11434"
    
    if llm_provider == "OpenAI":
        api_key = st.text_input("OpenAI API Key", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    else:
        st.info("Ensure Ollama is running locally: `ollama run llama3`")
        local_model = st.text_input("Model Name", "llama3")
        local_url = st.text_input("Base URL", "http://localhost:11434")
    
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

# Display generated chart if it exists and is recent (naive check)
if os.path.exists(IMG_PATH):
    st.image(IMG_PATH, caption="Latest Stress Test Result")

if prompt := st.chat_input("Ask about cash, compliance, or stress tests..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            agent = get_agent(llm_provider, api_key, local_model, local_url)
            with st.spinner("Agent is thinking..."):
                response = agent.invoke({"input": prompt})
                st.markdown(response["output"])
                st.session_state.messages.append({"role": "assistant", "content": response["output"]})
                
                # Refresh if chart was just created
                if "stress_test_result.png" in response["output"] or "chart" in response["output"].lower():
                    if os.path.exists(IMG_PATH):
                        st.image(IMG_PATH, caption="Latest Stress Test Result")
                        
        except Exception as e:
            st.error(f"Error: {e}")
