# Skill: Compliance & Regulatory Check

## Description
This skill leverages a RAG (Retrieval-Augmented Generation) system to check specific compliance rules, FX controls, and cross-border transfer limits from the internal knowledge base.

## Tools
### `check_compliance`
- **Input**: `query` (str) - Natural language query (e.g., "restrictions on BRL remittance").
- **Output**: Relevant excerpts from compliance documents.
- **Source Script**: `rag_check.py`

## Usage
Use this skill when the user asks about:
- "Is it legal to send money to [Country]?"
- "What are the reporting requirements for large transactions?"
- "Brazil FX rules."
