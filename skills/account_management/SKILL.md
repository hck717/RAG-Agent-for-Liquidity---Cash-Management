# Skill: Account Balance Management

## Description
This skill allows the agent to query internal SQL databases to retrieve real-time account balances for different currencies and entities.

## Tools
### `get_account_balance`
- **Input**: `currency` (str) - e.g., 'USD', 'HKD', 'BRL'.
- **Output**: Returns the account ID and balance formatted as a string.
- **Source Script**: `query_balance.py`

## Usage
Use this skill when the user asks about:
- "How much money do we have in USD?"
- "Check the HKD account balance."
- "Do we have enough funds for a transfer?"
