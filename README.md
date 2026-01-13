# RAG Agent for Liquidity & Cash Management (POC)

A conversational AI agent designed for Corporate Treasury teams to automate liquidity queries, compliance checks, and financial stress testing. This Proof of Concept (POC) demonstrates a "Plan-and-Execute" agentic architecture that combines RAG (Retrieval-Augmented Generation), SQL database querying, and Python-based simulations.

![Agent UI Screenshot](https://img.shields.io/badge/Status-POC-yellow) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

## 🚀 Key Features

*   **📈 Real-time Balance Checking**: Queries a local SQL database to retrieve up-to-date account balances.
*   **⚖️ Compliance & Regulatory Check (RAG)**: Retrieves foreign exchange (FX) rules using Vector Search (ChromaDB).
*   **⚠️ Agentic Stress Testing**: Runs Python simulations to forecast cash flow under stress scenarios and generates charts.
*   **🔒 Data Privacy First**: Supports **Local LLMs (Ollama)** via Docker integration.

## 🐳 Docker Quick Start (Recommended)

Run the entire application in an isolated container without installing Python dependencies locally.

### Prerequisites
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
*   [Ollama](https://ollama.com/) installed for local models.

### 1. Prepare Local Model (One-time setup)
Open your terminal and pull the **Llama 3.2** model (recommended for tool calling support).
```bash
ollama run llama3.2
```
*Note: We previously recommended `gemma3:1b`, but it does not support tool calling. Use `llama3.2` or `mistral-nemo`.*

### 2. Build and Run
Navigate to the project folder and start the container:

```bash
cd RAG-Agent-for-Liquidity---Cash-Management
docker-compose up --build
```
This command will:
1.  Build the Docker image.
2.  Initialize the databases automatically.
3.  Launch the Streamlit app on port 8501.

### 3. Access the Agent
Open your browser and navigate to:
[http://localhost:8501](http://localhost:8501)

### 4. Configure Agent for Local LLM
In the Agent Sidebar:
*   Select **"Local (Ollama)"**.
*   **Base URL**: Use `http://host.docker.internal:11434` (Docker handles the connection to your host machine).
*   **Model**: Type `llama3.2` (Default).

---

## 💡 Example Queries (Try These!)

Copy and paste these inputs into the chat to see the different capabilities of the Agent:

### 1. Simple Liquidity Check (SQL)
> "What is the current balance in our HKD account?"
*Demonstrates querying the local SQL database for real-time financial data.*

### 2. Regulatory Compliance Check (RAG)
> "What are the documentation requirements for inbound payments to Brazil?"
*Demonstrates searching the internal knowledge base (PDF/Docs) using Vector Search.*

### 3. Stress Test Simulation (Python)
> "Run a stress test: interest rate -2% and 30-day payment delay."
*Demonstrates generating a Python simulation and rendering a Matplotlib chart.*

### 4. Plan-and-Execute (Complex)
> "I need to send 5M USD to Brazil. Do we have enough funds and what are the rules?"
*Demonstrates the agent's ability to break down a complex request, check balances (Skill 1), check compliance (Skill 2), and synthesize a final answer.*

### 5. Scenario Analysis
> "Simulate a 45-day sales delay. Will we go negative?"
*Demonstrates interpreting simulation results to provide strategic advice.*

---

## 🛠️ Local Installation (Alternative)

If you prefer running without Docker:

1.  **Create Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run System**:
    ```bash
    python initialize_system.py
    streamlit run main.py
    ```

## 📂 Project Architecture

```text
RAG-Agent-for-Liquidity---Cash-Management/
├── Dockerfile                # 🐳 Container definition
├── docker-compose.yml        # 🐳 Service orchestration
├── main.py                   # 🧠 Core Agent Logic
├── initialize_system.py      # ⚙️ Setup Script
├── financial_data.db         # 🗄️ SQL DB (Persisted via Volume)
├── chroma_db/                # 🗄️ Vector DB (Persisted via Volume)
└── skills/                   # 🛠️ Modular Capabilities
    ├── account_management/
    ├── compliance/
    └── stress_testing/
```

## 📜 License
MIT
