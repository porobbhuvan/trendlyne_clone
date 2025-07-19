# symbol_fetcher.py

import pandas as pd

def get_local_symbols(filename="nse_symbols.csv"):
    try:
        df = pd.read_csv(filename)
        symbols = df["SYMBOL"].dropna().unique().tolist()
        return symbols
    except Exception as e:
        print(f"❌ Error loading symbols: {e}")
        return []

if __name__ == "__main__":
    symbols = get_local_symbols()
    print(f"✅ Loaded {len(symbols)} symbols.")
    print("🔍 Sample:", symbols[:10])
