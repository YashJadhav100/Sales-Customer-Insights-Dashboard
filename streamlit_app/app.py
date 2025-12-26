import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Sales & Customer Insights Dashboard",
    layout="wide"
)

# ----------------------------
# Load Data (Cloud-safe paths)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "monthly_revenue_trend.xlsx")

df = pd.read_excel(DATA_PATH)

# Ensure correct data types
df["Month"] = pd.to_datetime(df["Month"])
df["Year"] = df["Month"].dt.year
df["Month_Name"] = df["Month"].dt.strftime("%b %Y")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.title("Filters")
selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Year"].unique()),
    index=0
)

df_year = df[df["Year"] == selected_year].copy()

# ----------------------------
# Header
# ----------------------------
st.title("📊 Sales & Customer Insights Dashboard")
st.caption("Monthly revenue performance and growth analysis")

st.divider()

# ----------------------------
# KPI Metrics
# ----------------------------
total_revenue = df_year["Revenue"].sum()
avg_monthly_revenue = df_year["Revenue"].mean()
best_month = df_year.loc[df_year["Revenue"].idxmax(), "Month_Name"]

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Avg Monthly Revenue", f"${avg_monthly_revenue:,.0f}")
col3.metric("Best Month", best_month)

st.divider()

# ----------------------------
# Monthly Revenue Trend (Line)
# ----------------------------
st.subheader("📈 Monthly Revenue Trend")

fig_trend = px.line(
    df_year,
    x="Month",
    y="Revenue",
    markers=True,
    labels={"Revenue": "Revenue ($)", "Month": "Month"},
)

fig_trend.update_layout(
    height=450,
    yaxis_tickprefix="$",
)

st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# ----------------------------
# Month-over-Month Growth (%)
# ----------------------------
st.subheader("📊 Month-over-Month Revenue Growth (%)")

df_year["MoM_Growth"] = df_year["Revenue"].pct_change() * 100

# CLEAN NaN & Inf for Cloud stability
df_mom = df_year.dropna(subset=["MoM_Growth"])

if df_mom.empty:
    st.warning("Not enough data to calculate MoM growth.")
else:
    fig_mom = px.bar(
        df_mom,
        x="Month_Name",
        y="MoM_Growth",
        labels={
            "MoM_Growth": "Growth (%)",
            "Month_Name": "Month"
        },
    )

    fig_mom.update_layout(
        height=450,
        yaxis_ticksuffix="%",
    )

    st.plotly_chart(fig_mom, use_container_width=True)

st.divider()

# ----------------------------
# Data Preview
# ----------------------------
with st.expander("📄 View Data"):
    st.dataframe(df_year, use_container_width=True)
