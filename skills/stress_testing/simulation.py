import matplotlib.pyplot as plt
import os

IMG_PATH = "stress_test_result.png"

def execute_stress_test(rate_drop_percent: float, receivables_delay_days: int) -> str:
    """
    Run a liquidity stress test simulation and generate a forecast chart.
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
        
        # 4. Interest Rate Impact
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
