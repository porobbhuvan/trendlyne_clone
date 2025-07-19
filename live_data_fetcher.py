# live_data_fetcher.py

import yfinance as yf
import pandas as pd
from symbol_fetcher import get_local_symbols
import time

def fetch_fundamentals(symbols, limit=100):
    data = []

    for i, sym in enumerate(symbols[:limit]):  # Limit to 100 to avoid throttling
        try:
            stock = yf.Ticker(sym)
            info = stock.info

            data.append({
                "Symbol": sym,
                "Name": info.get("shortName"),
                "Price": info.get("currentPrice"),
                "EPS (Fwd)": info.get("forwardEps"),
                "PE Ratio": info.get("forwardPE"),
                "Dividend Yield": info.get("dividendYield"),
                "Target Price": info.get("targetMeanPrice"),
                "Recommendation": info.get("recommendationKey"),
                "Market Cap": info.get("marketCap"),
                "Sector": info.get("sector"),
                "Industry": info.get("industry"),
                "Beta": info.get("beta"),
                "P/B Ratio": info.get("priceToBook"),
                "Book Value": info.get("bookValue"),
                "ROE": info.get("returnOnEquity"),
                "Revenue Growth": info.get("revenueGrowth"),
                "EPS Growth": info.get("earningsGrowth")
            })


            print(f"[{i+1}] ✅ {sym} fetched")
            time.sleep(1)  # Sleep to avoid rate limiting

        except Exception as e:
            print(f"[{i+1}] ❌ Failed for {sym}: {e}")

    df = pd.DataFrame(data)
    df.to_csv("fundamentals_snapshot.csv", index=False)
    print("✅ Saved to fundamentals_snapshot.csv")
    return df

if __name__ == "__main__":
    symbols = get_local_symbols("nse_symbols.csv")
    fetch_fundamentals(symbols, limit=3000)  # you can raise the limit gradually
