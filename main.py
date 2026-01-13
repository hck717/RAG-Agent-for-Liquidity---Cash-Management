import streamlit as st
import os
import sys

# Add the repository root to sys.path to allow importing from skills
sys.path.append(os.getcwd())

# Modern LangGraph Implementation
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

# Import Skills
from skills.account_management.query_balance import execute_query
from skills.compliance.rag_check import execute_rag_check
from skills.stress_testing.simulation import execute_stress_test

# --- Configuration ---
IMG_PATH = "stress_test_result.png"

# DEFAULT MODEL CHANGED to llama3.2 which supports tool calling
DEFAULT_MODEL = "llama3.2" 

st.set_page_config(page_title="Liquidity & Cash Management Agent", layout="wide")

# --- Define Tools Wrappers ---
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

# --- System Prompt ---
SYSTEM_PROMPT = """You are an expert Corporate Treasury AI Agent.

Your goal is to assist with liquidity management, compliance checks, and stress testing.

**Instructions for Complex Tasks (Plan and Execute):**
1. **Plan**: When a user asks a complex question (e.g., "Can I send money?"), first analyze what information is missing.
   - Do you know the account balance? (Call `get_account_balance`)
   - Do you know the compliance rules? (Call `check_compliance_rules`)
2. **Execute**: Call the necessary tools one by one.
3. **Analyze**: Combine the outputs to form a final answer.

**Instructions for Stress Testing:**
- If the user asks for a stress test, identify the variables (Interest Rate Change, Payment Delay Days).
- If values are missing, ask the user or assume reasonable defaults (and state them).
- Call `run_stress_test`.
- ALWAYS mention that a chart has been generated and displayed.

**General:**
- Always cite your sources (e.g., "According to the database...", "The compliance rules state...").
"""

# --- Agent Setup ---
def get_agent(llm_choice, openai_api_key=None, local_model_name=DEFAULT_MODEL, local_base_url="http://host.docker.internal:11434"):
    tools = [get_account_balance, check_compliance_rules, run_stress_test]
    
    if llm_choice == "OpenAI":
        if not openai_api_key:
            raise ValueError("OpenAI API Key is required for OpenAI models.")
        llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=openai_api_key)
    else:
        # Local (Ollama)
        # Note: Model must support tool calling (e.g., llama3.1, llama3.2, mistral-nemo)
        llm = ChatOllama(model=local_model_name, base_url=local_base_url, temperature=0)
    
    # Create the ReAct agent
    agent_graph = create_react_agent(llm, tools)
    return agent_graph

# --- Helper to safely display image ---
def display_stress_test_chart():
    """Checks if the chart exists and is valid before rendering."""
    if os.path.exists(IMG_PATH) and os.path.getsize(IMG_PATH) > 0:
        try:
            st.image(IMG_PATH, caption="Latest Stress Test Result")
        except Exception:
            pass

# --- UI Layout ---
st.title("💰 Corporate Treasury AI Agent")
st.markdown("POC: Liquidity Management & Compliance Checker")
st.caption("Powered by Agentic Skills: `Account Management`, `Compliance Check`, `Stress Testing`")

# Sidebar for Config
with st.sidebar:
    st.header("Settings")
    llm_provider = st.radio("LLM Provider", ["OpenAI", "Local (Ollama)"])
    
    api_key = ""
    # Retrieve default from env or use the Docker-friendly default
    default_url = os.environ.get("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    
    if llm_provider == "OpenAI":
        api_key = st.text_input("OpenAI API Key", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    else:
        st.warning("⚠️ Requirement: Use a model that supports Tool Calling (e.g., llama3.2, llama3.1, mistral-nemo).")
        st.info("Run: `ollama run llama3.2`")
        
        # Default to llama3.2 which is small, fast, and supports tools
        local_model = st.text_input("Model Name", DEFAULT_MODEL)
        local_url = st.text_input("Base URL", value=default_url)
    
    st.markdown("---")
    if st.button("Initialize System (Reset DBs)"):
        with st.spinner("Initializing databases..."):
            os.system("python initialize_system.py")
            if os.path.exists(IMG_PATH):
                try:
                    os.remove(IMG_PATH)
                except:
                    pass
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

# --- Fix: Safer Image Rendering ---
display_stress_test_chart()

if prompt := st.chat_input("Ask about cash, compliance, or stress tests..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Pass the configured URL from the sidebar
            agent = get_agent(llm_provider, api_key, local_model, local_url)
            with st.spinner("Agent is thinking..."):
                inputs = {
                    "messages": [
                        SystemMessage(content=SYSTEM_PROMPT),
                        HumanMessage(content=prompt)
                    ]
                }
                
                response = agent.invoke(inputs)
                
                final_content = response["messages"][-1].content
                
                st.markdown(final_content)
                st.session_state.messages.append({"role": "assistant", "content": final_content})
                
                if "stress_test_result.png" in final_content or "chart" in final_content.lower():
                     display_stress_test_chart()
                        
        except Exception as e:
            if "does not support tools" in str(e):
                st.error("❌ Model Error: The selected model does not support tool calling. Please use `llama3.2` or `llama3.1`.")
            else:
                st.error(f"Error: {e}")
