# filter_engine.py

import pandas as pd

def apply_named_filter(df, filter_name):
    if filter_name == "High Bullishness":
        return df[(df["Target Price"] > df["Price"] * 1.2) & (df["Recommendation"] == "buy")]

    elif filter_name == "Strong Buy Rated":
        return df[(df["Recommendation"] == "strong_buy") & (df["EPS Growth"] > 0.10)]

    elif filter_name == "High EPS Growth":
        return df[(df["EPS Growth"] > 0.15) & (df["PE Ratio"] < 25)]

    elif filter_name == "Top ROE Stocks":
        return df[(df["ROE"] > 0.2) & (df["PE Ratio"] < 20) & (df["Dividend Yield"] > 0.01)]

    elif filter_name == "Low PE, High Growth":
        return df[(df["PE Ratio"] < 15) & (df["EPS Growth"] > 0.10) & (df["ROE"] > 0.15)]

    elif filter_name == "Oversold Stocks":
        return df[(df["PE Ratio"] < 10) & (df["Dividend Yield"] > 0.02)]

    elif filter_name == "Turnaround Stocks":
        return df[(df["EPS Growth"] > 0.01) & (df["Price"] < df["Target Price"])]

    else:
        return df

def load_fundamentals(filename="fundamentals_snapshot.csv"):
    return pd.read_csv(filename)

def filter_buy_recommendations(df):
    return df[df["Recommendation"] == "buy"]

def filter_eps_growth(df, min_growth=0.1):
    return df[df["EPS Growth"] > min_growth]

def filter_high_dividend(df, min_yield=0.02):
    return df[df["Dividend Yield"] >= min_yield]

def filter_value_stocks(df, max_pe=15, min_roe=0.15):
    return df[(df["PE Ratio"] < max_pe) & (df["ROE"] > min_roe)]

def filter_custom(df, **kwargs):
    """Apply any custom logic using kwargs. Example: Beta, Sector, etc."""
    for col, (op, val) in kwargs.items():
        if op == ">":
            df = df[df[col] > val]
        elif op == "<":
            df = df[df[col] < val]
        elif op == "==":
            df = df[df[col] == val]
    return df

if __name__ == "__main__":
    df = load_fundamentals()

    print("🟢 Buy Rated:")
    print(filter_buy_recommendations(df)[["Symbol", "Recommendation", "Target Price", "Price"]].head())

    print("\n📈 EPS Growth > 10%:")
    print(filter_eps_growth(df).head())
