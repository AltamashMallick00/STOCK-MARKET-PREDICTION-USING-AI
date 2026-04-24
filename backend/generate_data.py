import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(symbol="AAPL", days=1000):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # Generate random walk data
    price = 150.0
    prices = []
    for _ in range(len(dates)):
        change = np.random.normal(0, 2)
        price += change
        prices.append(max(10, price))
        
    df = pd.DataFrame({
        'Date': dates,
        'Open': [p * (1 + np.random.normal(0, 0.01)) for p in prices],
        'High': [p * (1 + abs(np.random.normal(0, 0.02))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.02))) for p in prices],
        'Close': prices,
        'Volume': np.random.randint(1000000, 5000000, size=len(dates))
    })
    
    import os
    os.makedirs('backend/data', exist_ok=True)
    df.to_csv(f'backend/data/{symbol}.csv', index=False)
    print(f"Generated sample data for {symbol} in backend/data/{symbol}.csv")

def generate_all_mncs():
    mncs = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NFLX"]
    for symbol in mncs:
        generate_sample_data(symbol)

if __name__ == "__main__":
    generate_all_mncs()
