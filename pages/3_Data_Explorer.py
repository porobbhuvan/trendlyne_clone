import streamlit as st
import pandas as pd
from filter_engine import load_fundamentals

st.title("📂 Full Data Explorer")

df = load_fundamentals()

search = st.text_input("🔍 Search by Symbol or Name").lower()
sector = st.selectbox("📁 Filter by Sector (optional)", ["All"] + sorted(df["Sector"].dropna().unique()))

filtered_df = df.copy()

if sector != "All":
    filtered_df = filtered_df[filtered_df["Sector"] == sector]

if search:
    filtered_df = filtered_df[
        filtered_df["Symbol"].str.lower().str.contains(search) |
        filtered_df["Name"].str.lower().str.contains(search)
    ]

st.markdown(f"Showing **{len(filtered_df)}** matching stocks")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

st.download_button(
    label="📥 Download This View",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="explorer_filtered.csv",
    mime="text/csv"
)
