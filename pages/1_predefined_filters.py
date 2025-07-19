import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from filter_engine import load_fundamentals, apply_named_filter

st.title("🧠 Predefined Filters — Trendlyne Style")

df = load_fundamentals()

filter_options = [
    "High Bullishness",
    "Strong Buy Rated",
    "High EPS Growth",
    "Top ROE Stocks",
    "Low PE, High Growth",
    "Oversold Stocks",
    "Turnaround Stocks"
]

selected_filter = st.selectbox("🔽 Select a Strategy", filter_options)
filtered_df = apply_named_filter(df, selected_filter)

# Market Cap Filter
market_caps = ["All", "Large Cap", "Mid Cap", "Small Cap"]
selected_cap = st.selectbox("🏦 Filter by Market Cap", market_caps)

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


# Sector filter
sectors = ["All"] + sorted(filtered_df["Sector"].dropna().unique())
selected_sector = st.selectbox("📁 Filter by Sector (optional)", sectors)

if selected_sector != "All":
    filtered_df = filtered_df[filtered_df["Sector"] == selected_sector]

st.subheader(f"Results for: **{selected_filter}**")
st.markdown(f"Found **{len(filtered_df)}** matching stocks.")

for idx, row in filtered_df.iterrows():
    col1, col2 = st.columns([2, 3])
    with col1:
        roe_display = f"{row['ROE']:.2%}" if pd.notna(row['ROE']) else "N/A"
        st.markdown(f"""
        ### 💼 {row['Symbol']}
        - 🏷 **Name**: {row['Name']}
        - 💰 **Price**: ₹{row['Price']}
        - 🎯 **Target**: ₹{row['Target Price']}
        - ✅ **Reco**: {row['Recommendation'].capitalize()}
        - 📈 **EPS Growth**: {row['EPS Growth']:.2%}
        - 📊 **PE**: {row['PE Ratio']}
        - 🧠 **ROE**: {roe_display}
        """)



    with col2:
        if pd.notna(row['Target Price']) and pd.notna(row['Price']):
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=["Current Price", "Target Price"],
                y=[row['Price'], row['Target Price']],
                marker_color=["#1f77b4", "#2ca02c"]
            ))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

st.download_button(
    f"📥 Download Filtered Stocks",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name=f"{selected_filter.replace(' ', '_')}.csv",
    mime="text/csv"
)