import streamlit as st
import os
import sys

# Add the repository root to sys.path to allow importing from skills
sys.path.append(os.getcwd())

# Fix: Import AgentExecutor from the new location in newer LangChain versions if needed, 
# or explicit sub-module for older/newer compatibility. 
# Attempting direct import first, but falling back to specific module structure.
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import Skills
from skills.account_management.query_balance import execute_query
from skills.compliance.rag_check import execute_rag_check
from skills.stress_testing.simulation import execute_stress_test

# --- Configuration ---
IMG_PATH = "stress_test_result.png"

st.set_page_config(page_title="Liquidity & Cash Management Agent", layout="wide")

# --- Define Tools Wrappers ---
# These wrappers expose the modular skill scripts as Agent Tools

@tool
def get_account_balance(currency: str):
    """Query the SQL database to find the account balance for a specific currency."""
    return execute_query(currency)

@tool
def check_compliance_rules(query: str):
    """Search the knowledge base (RAG) for compliance guidelines, specifically for FX and cross-border transfers."""
    return execute_rag_check(query)

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
    return execute_stress_test(rate_drop_percent, receivables_delay_days)

# --- Agent Setup ---
def get_agent(llm_choice, openai_api_key=None, local_model_name="gemma3:1b", local_base_url="http://localhost:11434"):
    tools = [get_account_balance, check_compliance_rules, run_stress_test]
    
    if llm_choice == "OpenAI":
        if not openai_api_key:
            raise ValueError("OpenAI API Key is required for OpenAI models.")
        llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=openai_api_key)
    else:
        # Local (Ollama)
        llm = ChatOllama(model=local_model_name, base_url=local_base_url, temperature=0)

    # Agent System Prompt designed for "Plan and Execute" mindset
    system_prompt = """You are an expert Corporate Treasury AI Agent.
    
    Your goal is to assist with liquidity management, compliance checks, and stress testing.
    
    **Instructions for Complex Tasks (Plan and Execute):**
    1. **Plan**: When a user asks a complex question (e.g., "Can I send money?"), first analyze what information is missing.
       - Do you know the account balance? (Call `get_account_balance`)
       - Do you know the compliance rules? (Call `check_compliance_rules`)
    2. **Execute**: Call the necessary tools one by one.
    3. **Analyze**: Combine the outputs (e.g., "Balance is $4M, but Limit is $10k") to form a final answer.
    
    **Instructions for Stress Testing:**
    - If the user asks for a stress test, identify the variables (Interest Rate Change, Payment Delay Days).
    - If values are missing, ask the user or assume reasonable defaults (and state them).
    - Call `run_stress_test`.
    - ALWAYS mention that a chart has been generated and displayed.
    
    **General:**
    - Always cite your sources (e.g., "According to the database...", "The compliance rules state...").
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

# --- UI Layout ---
st.title("💰 Corporate Treasury AI Agent")
st.markdown("POC: Liquidity Management & Compliance Checker")
st.caption("Powered by Agentic Skills: `Account Management`, `Compliance Check`, `Stress Testing`")

# Sidebar for Config
with st.sidebar:
    st.header("Settings")
    llm_provider = st.radio("LLM Provider", ["OpenAI", "Local (Ollama)"])
    
    api_key = ""
    local_model = "gemma3:1b"
    local_url = "http://localhost:11434"
    
    if llm_provider == "OpenAI":
        api_key = st.text_input("OpenAI API Key", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    else:
        st.info("Ensure Ollama is running locally: `ollama run gemma3:1b`")
        local_model = st.text_input("Model Name", "gemma3:1b")
        local_url = st.text_input("Base URL", "http://localhost:11434")
    
    st.markdown("---")
    if st.button("Initialize System (Reset DBs)"):
        with st.spinner("Initializing databases..."):
            os.system("python initialize_system.py")
            st.success("System Initialized!")

    st.markdown("---")
    st.header("💡 Try These Queries")
    st.markdown("""
    **1. Check Balance (SQL)**
    > "What is the current balance in our HKD account?"
    
    **2. Compliance Check (RAG)**
    > "What are the documentation requirements for inbound payments to Brazil?"
    
    **3. Stress Test (Simulation)**
    > "Run a stress test: interest rate -2% and 30-day payment delay."
    
    **4. Plan & Execute (Complex)**
    > "I need to send 5M USD to Brazil. Do we have enough funds and what are the rules?"
    
    **5. Scenario Analysis**
    > "Simulate a 45-day sales delay. Will we go negative?"
    """)

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
