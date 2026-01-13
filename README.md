# RAG Agent for Liquidity & Cash Management (POC)

A conversational AI agent designed for Corporate Treasury teams to automate liquidity queries, compliance checks, and financial stress testing. This Proof of Concept (POC) demonstrates a "Plan-and-Execute" agentic architecture that combines RAG (Retrieval-Augmented Generation), SQL database querying, and Python-based simulations.

![Agent UI Screenshot](https://img.shields.io/badge/Status-POC-yellow) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![LangChain](https://img.shields.io/badge/LangChain-v0.1-green)

## 🚀 Key Features

*   **📈 Real-time Balance Checking**: Queries a local SQL database to retrieve up-to-date account balances across multiple currencies.
*   **⚖️ Compliance & Regulatory Check (RAG)**: Retrieves foreign exchange (FX) rules and cross-border transfer limits from an internal knowledge base (PDF/Markdown) using Vector Search (ChromaDB).
*   **⚠️ Agentic Stress Testing**:
    *   **Simulation**: Runs Python simulations to forecast cash flow under stress scenarios (e.g., Interest Rate Drops, Payment Delays).
    *   **Visualization**: Automatically generates and displays charts (Matplotlib) to visualize liquidity trends.
*   **🔒 Data Privacy First**: Supports **Local LLMs (Ollama/Llama 3)** and local embeddings to ensure sensitive financial data never leaves your infrastructure.

## 📂 Project Architecture: Agent Skills

This project follows a modular **Agentic Skills** architecture. Each capability is encapsulated in the `skills/` directory with its own documentation and logic.

```text
RAG-Agent-for-Liquidity---Cash-Management/
├── main.py                   # 🧠 Core Agent Logic (Streamlit UI + LangChain)
├── initialize_system.py      # ⚙️ Setup Script (Seeds SQL DB & Vector DB)
├── financial_data.db         # 🗄️ Local SQLite DB (Mock Balances)
├── chroma_db/                # 🗄️ Local Vector DB (Compliance Docs)
└── skills/                   # 🛠️ Modular Capabilities
    ├── account_management/   # SQL Querying for Balances
    ├── compliance/           # RAG System for Regulatory Checks
    └── stress_testing/       # Python Simulation & Plotting
```

## 🛠️ Tech Stack

*   **LLM Orchestration**: [LangChain](https://python.langchain.com/) (Tools, Agents)
*   **Interface**: [Streamlit](https://streamlit.io/)
*   **Database**: SQLite (Transactional), ChromaDB (Vector Store)
*   **Models**: 
    *   **OpenAI** (GPT-4o) - *Optional*
    *   **Ollama** (Llama 3, Mistral) - *Supported for Local Privacy*
*   **Visualization**: Matplotlib

## ⚡ Quick Start

### Prerequisites
*   Python 3.10+
*   (Optional) [Ollama](https://ollama.com/) installed for local model support.

### 1. Installation

```bash
git clone https://github.com/hck717/RAG-Agent-for-Liquidity---Cash-Management.git
cd RAG-Agent-for-Liquidity---Cash-Management
pip install -r requirements.txt
```

### 2. System Initialization
Run this script once to create the mock SQL database and ingest the sample compliance documents into the Vector DB.

```bash
python initialize_system.py
```
*Note: If you don't have an `OPENAI_API_KEY` set, this script will automatically default to using local HuggingFace embeddings.*

### 3. Run the Agent

```bash
streamlit run main.py
```

## 📖 Usage Guide

The Agent supports two modes: **OpenAI** (Cloud) and **Local (Ollama)**. You can switch between them in the sidebar.

### Scenario 1: Cross-Border Transfer
**User**: *"I want to send 5 Million USD from Hong Kong to Brazil. Are there any restrictions?"*

**Agent Action (Plan & Execute)**:
1.  **Check Balance**: Queries SQL DB -> *Finds Account Balance is $4M USD (Insufficient).*
2.  **Check Compliance**: Queries RAG -> *Finds Brazil requires reporting for inflows >$10k and IOF tax applies.*
3.  **Response**: *"You have insufficient funds ($4M vs $5M required). Additionally, Brazil requires an exchange contract for this amount..."*

### Scenario 2: Liquidity Stress Test
**User**: *"Run a stress test if HKD interest rate drops by 2% and our Brazil sales are delayed by 30 days."*

**Agent Action**:
1.  **Identify Variables**: Rate Change (-2%), Delay (+30 days).
2.  **Run Simulation**: Calls `skills/stress_testing/simulation.py`.
3.  **Visualize**: Generates `stress_test_result.png`.
4.  **Response**: Displays the chart and warns: *"Critical: Liquidity turns negative on Day 15. You need to draw down $2M from the revolver."*

## 🔧 Configuration

*   **Environment Variables**: Create a `.env` file or set via terminal for OpenAI usage:
    ```bash
    export OPENAI_API_KEY="sk-..."
    ```
*   **Local Models**: Ensure your Ollama server is running (`ollama serve`). default URL is `http://localhost:11434`.

## 📜 License
MIT
