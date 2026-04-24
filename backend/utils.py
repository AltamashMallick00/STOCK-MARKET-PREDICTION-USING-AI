import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def load_stock_data(symbol):
    file_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    if not os.path.exists(file_path):
        return None
    return pd.read_csv(file_path)

def get_available_stocks():
    files = os.listdir(DATA_DIR)
    return [f.replace('.csv', '') for f in files if f.endswith('.csv')]
