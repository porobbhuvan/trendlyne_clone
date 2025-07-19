# 📁 trendlyne_clone/app.py
import streamlit as st

st.set_page_config(page_title="Trendlyne Clone", layout="wide")

st.title("📊 Welcome to Trendlyne Clone")
st.markdown("""
This is your custom-built **fundamental screener** for Indian stocks.  
Use the navigation menu to explore:

- 🔍 Predefined strategies (like High Bullishness, Top ROE)
- ⚙️ Custom filter builder
- 📂 Data explorer

Built using **Streamlit + Python + yfinance**. You can customize, expand, and even score stocks with AI in the next steps.
""")
