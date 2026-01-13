# Skill: Liquidity Stress Test Simulation

## Description
This skill allows the agent to run complex Python simulations to forecast cash flow under stress scenarios (e.g., interest rate shocks, payment delays).

## Tools
### `run_stress_test`
- **Input**: 
    - `rate_drop_percent` (float): Interest rate decrease (e.g., 2.0).
    - `receivables_delay_days` (int): Number of days sales are delayed (e.g., 30).
- **Output**: A text summary of the minimum liquidity balance and potential overdrafts. 
- **Side Effect**: Generates a plot saved as `stress_test_result.png`.
- **Source Script**: `simulation.py`

## Usage
Use this skill when the user asks:
- "What happens if rates drop by 2%?"
- "Run a stress test for a 30-day payment delay."
- "Simulate our cash flow next month."
