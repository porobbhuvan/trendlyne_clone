import streamlit as st
import pandas as pd
from filter_engine import load_fundamentals

st.title("⚙️ Custom Filter Builder")

df = load_fundamentals()
filtered_df = df.copy()

st.sidebar.header("🧰 Build Your Filter")

# EPS Growth
if st.sidebar.checkbox("EPS Growth Filter"):
    min_eps = st.sidebar.slider("Minimum EPS Growth (%)", 0, 100, 10)
    filtered_df = filtered_df[filtered_df["EPS Growth"] * 100 >= min_eps]

# PE Ratio
if st.sidebar.checkbox("PE Ratio Filter"):
    max_pe = st.sidebar.slider("Maximum PE Ratio", 0, 100, 25)
    filtered_df = filtered_df[filtered_df["PE Ratio"] <= max_pe]

# ROE Filter
if st.sidebar.checkbox("ROE Filter"):
    min_roe = st.sidebar.slider("Minimum ROE (%)", 0.0, 100.0, 15.0)
    filtered_df = filtered_df[filtered_df["ROE"] * 100 >= min_roe]

# Dividend Yield
if st.sidebar.checkbox("Dividend Yield Filter"):
    min_div = st.sidebar.slider("Minimum Dividend Yield (%)", 0.0, 10.0, 1.0)
    filtered_df = filtered_df[filtered_df["Dividend Yield"] * 100 >= min_div]

# Sector Filter
sectors = ["All"] + sorted(df["Sector"].dropna().unique())
selected_sector = st.sidebar.selectbox("📁 Sector", sectors)
if selected_sector != "All":
    filtered_df = filtered_df[filtered_df["Sector"] == selected_sector]

# Market Cap Filter
market_caps = ["All", "Large Cap", "Mid Cap", "Small Cap"]
selected_cap = st.sidebar.selectbox("🏦 Market Cap", market_caps)

def apply_market_cap_filter(df, cap_choice):
    if cap_choice == "Large Cap":
        return df[df["Market Cap"] > 20000]
    elif cap_choice == "Mid Cap":
        return df[(df["Market Cap"] >= 5000) & (df["Market Cap"] <= 20000)]
    elif cap_choice == "Small Cap":
        return df[df["Market Cap"] < 5000]
    else:
        return df

filtered_df = apply_market_cap_filter(filtered_df, selected_cap)

# Recommendation Filter
if st.sidebar.checkbox("Only Show Buy / Strong Buy"):
    filtered_df = filtered_df[filtered_df["Recommendation"].isin(["buy", "strong_buy"])]

# Final Output
st.subheader(f"🔎 Filtered Stocks ({len(filtered_df)})")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="custom_filtered_stocks.csv",
    mime="text/csv"
)
