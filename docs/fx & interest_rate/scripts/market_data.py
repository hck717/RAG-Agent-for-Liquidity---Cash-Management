import yfinance as yf
import pandas as pd

def get_market_rates():
    """
    Fetches real-time FX spot rates and reference interest rates (Treasury Yields)
    using yfinance. Returns a dictionary and a formatted string for the Agent.
    """
    print("⏳ Fetching real-time data from Yahoo Finance...")

    # --- 1. Define Tickers ---
    # Yahoo Finance Ticker Symbols
    tickers = {
        # FX Pairs (Quote is usually USD based)
        "USDHKD=X": "USD/HKD",
        "CNY=X": "USD/CNY",      # Note: Yahoo often lists as USD/CNY directly
        "BRL=X": "USD/BRL",
        "EURUSD=X": "EUR/USD",
        "GBPUSD=X": "GBP/USD",
        
        # Interest Rate Proxies (Risk-Free Rates)
        "^IRX": "USD_3M_Bill_Yield",  # Proxy for short-term USD cash rate
        "^TNX": "USD_10Y_Note_Yield"  # Proxy for long-term cost of capital
    }
    
    # --- 2. Bulk Download Data ---
    # period='1d' fetches the latest trading day
    data = yf.download(list(tickers.keys()), period="1d", group_by='ticker', progress=False)
    
    market_snapshot = {}
    
    # --- 3. Parse Results ---
    for symbol, friendly_name in tickers.items():
        try:
            # Check if we have data for this symbol
            if symbol in data.columns.levels[0]:
                # Get the last available 'Close' price
                latest_value = data[symbol]['Close'].iloc[-1]
                
                # Formatting: Yields are %, FX are decimals
                if "Yield" in friendly_name:
                    market_snapshot[friendly_name] = f"{latest_value:.2f}%"
                else:
                    market_snapshot[friendly_name] = f"{latest_value:.4f}"
            else:
                market_snapshot[friendly_name] = "N/A"
        except Exception as e:
            market_snapshot[friendly_name] = "Error"

    # --- 4. Generate Agent-Friendly String ---
    report = (
        f"### REAL-TIME MARKET SNAPSHOT ###\n"
        f"Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"--- FX Spot Rates ---\n"
        f"USD/HKD: {market_snapshot.get('USD/HKD', 'N/A')}\n"
        f"USD/CNY: {market_snapshot.get('USD/CNY', 'N/A')}\n"
        f"USD/BRL: {market_snapshot.get('USD/BRL', 'N/A')}\n"
        f"EUR/USD: {market_snapshot.get('EUR/USD', 'N/A')}\n\n"
        f"--- Reference Interest Rates ---\n"
        f"USD 3M Rate (Risk-Free): {market_snapshot.get('USD_3M_Bill_Yield', 'N/A')}\n"
        f"USD 10Y Rate (Bond Yield): {market_snapshot.get('USD_10Y_Note_Yield', 'N/A')}\n"
    )
    
    return report

if __name__ == "__main__":
    # Ensure you have libraries installed: pip install yfinance pandas
    print(get_market_rates())
