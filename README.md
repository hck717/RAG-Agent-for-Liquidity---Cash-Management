# RAG Agent for Liquidity & Cash Management (POC)

A conversational AI agent designed for Corporate Treasury teams to automate liquidity queries, compliance checks, and financial stress testing. This Proof of Concept (POC) demonstrates a "Plan-and-Execute" agentic architecture that combines RAG (Retrieval-Augmented Generation), SQL database querying, and Python-based simulations.

![Agent UI Screenshot](https://img.shields.io/badge/Status-POC-yellow) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

## 🚀 Key Features

*   **📈 Real-time Balance Checking**: Queries a local SQL database to retrieve up-to-date account balances.
*   **⚖️ Compliance & Regulatory Check (RAG)**: Retrieves foreign exchange (FX) rules using Vector Search (ChromaDB).
*   **⚠️ Agentic Stress Testing**: Runs Python simulations to forecast cash flow under stress scenarios and generates charts.
*   **🔒 Data Privacy First**: Supports **Local LLMs (Ollama/Llama 3)** via Docker integration.

## 🐳 Docker Quick Start (Recommended)

Run the entire application in an isolated container without installing Python dependencies locally.

### Prerequisites
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
*   (Optional) [Ollama](https://ollama.com/) running locally for local models.

### 1. Build and Run
```bash
docker-compose up --build
```
This command will:
1.  Build the Docker image.
2.  Initialize the databases automatically.
3.  Launch the Streamlit app on port 8501.

### 2. Access the Agent
Open your browser and navigate to:
[http://localhost:8501](http://localhost:8501)

### 3. Using Local LLMs (Ollama)
If you are running Ollama on your host machine, simply select **"Local (Ollama)"** in the agent sidebar.
*   **Base URL**: Use `http://host.docker.internal:11434` (Docker handles this network bridge automatically).
*   **Model**: e.g., `llama3`.

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
